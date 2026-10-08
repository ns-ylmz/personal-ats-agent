"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ArrowLeft, Loader2, Sparkles, Target, MessageSquare, Send, Trash2 } from "lucide-react";

type JobDetail = {
  id: number;
  status: string;
  job_description: string | null;
  match_score: number | null;
  cover_letter: string | null;
  prep_questions: string[] | null;
};

export default function JobDetailPage() {
  const { id } = useParams();
  const router = useRouter();
  const [job, setJob] = useState<JobDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [feedback, setFeedback] = useState("");
  const [submittingFeedback, setSubmittingFeedback] = useState(false);
  const [isDescExpanded, setIsDescExpanded] = useState(false);

  useEffect(() => {
    const fetchJob = async () => {
      try {
        const res = await fetch(`http://localhost:8000/jobs/${id}`);
        if (res.ok) {
          const data = await res.json();
          setJob(data);
        }
      } catch (e) {
        console.error("Failed to fetch job", e);
      } finally {
        setLoading(false);
      }
    };
    if (id) fetchJob();
  }, [id]);

  const handleAddFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedback) return;
    setSubmittingFeedback(true);
    try {
      const res = await fetch(`http://localhost:8000/jobs/${id}/feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ feedback_text: feedback })
      });
      if (res.ok) {
        setFeedback("");
        alert("Feedback recorded! AI will learn from this for future jobs.");
      }
    } catch (e) {
      console.error(e);
    } finally {
      setSubmittingFeedback(false);
    }
  };

  const handleUpdateStatus = async (newStatus: string) => {
    try {
      const res = await fetch(`http://localhost:8000/jobs/${id}/status`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus })
      });
      if (res.ok) {
        const data = await res.json();
        setJob(data);
      }
    } catch (e) {
      console.error(e);
    }
  };

  const handleDeleteJob = async () => {
    if (!window.confirm("Are you sure you want to delete this job?")) return;
    try {
      const res = await fetch(`http://localhost:8000/jobs/${id}`, {
        method: "DELETE"
      });
      if (res.ok) {
        router.push("/");
      }
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
      </div>
    );
  }

  if (!job) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
        <h2 className="text-xl font-semibold mb-4">Job not found</h2>
        <Button onClick={() => router.push("/")}>Go Back</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-12">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="outline" size="icon" onClick={() => router.push("/")}>
              <ArrowLeft className="w-4 h-4" />
            </Button>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Application #{job.id}</h1>
              <div className="flex items-center gap-3 mt-1">
                <span className="text-sm font-medium text-gray-500">Status:</span>
                <select 
                  className="text-sm border-gray-300 rounded-md shadow-sm focus:border-blue-300 focus:ring focus:ring-blue-200 focus:ring-opacity-50"
                  value={job.status}
                  onChange={(e) => handleUpdateStatus(e.target.value)}
                >
                  <option value="PENDING">Pending</option>
                  <option value="COMPLETED">Analyzed</option>
                  <option value="APPLIED">Applied</option>
                  <option value="INTERVIEWING">Interviewing</option>
                  <option value="OFFER">Offer</option>
                  <option value="REJECTED">Rejected</option>
                </select>
              </div>
            </div>
          </div>
          <Button variant="destructive" size="sm" onClick={handleDeleteJob} className="flex items-center gap-2">
            <Trash2 className="w-4 h-4" />
            Delete
          </Button>
        </div>

        {/* Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Job Description */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="h-full">
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <BriefcaseIcon className="w-5 h-5 text-blue-600" />
                  Job Description
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className={`whitespace-pre-wrap text-sm text-gray-700 bg-gray-100/50 p-4 rounded-lg overflow-y-auto ${isDescExpanded ? 'max-h-full' : 'max-h-[300px]'}`}>
                  {job.job_description || "No description available."}
                </div>
                {job.job_description && job.job_description.length > 500 && (
                  <Button 
                    variant="ghost" 
                    className="w-full mt-2 text-blue-600 text-xs" 
                    onClick={() => setIsDescExpanded(!isDescExpanded)}
                  >
                    {isDescExpanded ? "Show Less" : "Read Full Description"}
                  </Button>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column: AI Preparation Studio */}
          <div className="lg:col-span-2 space-y-6">
            
            {/* Match Score & Cover Letter */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card className="md:col-span-1 flex flex-col justify-center items-center text-center p-6">
                <Target className="w-8 h-8 text-blue-500 mb-2" />
                <h3 className="text-sm font-medium text-gray-500">AI Match Score</h3>
                <p className="text-4xl font-bold text-gray-900 mt-2">
                  {job.match_score !== null ? `${job.match_score}%` : "-"}
                </p>
              </Card>

              <Card className="md:col-span-2">
                <CardHeader>
                  <CardTitle className="text-lg flex items-center gap-2">
                    <Sparkles className="w-5 h-5 text-amber-500" />
                    Cover Letter Draft
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="text-sm text-gray-700 max-h-[200px] overflow-y-auto">
                    {job.cover_letter || "Not generated yet."}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Prep Questions */}
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <MessageSquare className="w-5 h-5 text-green-600" />
                  Interview Prep Questions
                </CardTitle>
              </CardHeader>
              <CardContent>
                {job.prep_questions && job.prep_questions.length > 0 ? (
                  <ul className="space-y-3">
                    {job.prep_questions.map((q, idx) => (
                      <li key={idx} className="bg-white border border-gray-100 shadow-sm p-4 rounded-lg text-sm text-gray-800 flex gap-3">
                        <span className="font-bold text-gray-400">{idx + 1}.</span>
                        <span>{q}</span>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="text-sm text-gray-500">No preparation questions available.</p>
                )}
              </CardContent>
            </Card>

            {/* Post-Interview Feedback Loop */}
            <Card className="bg-blue-50/50 border-blue-100">
              <CardHeader>
                <CardTitle className="text-lg text-blue-900">Post-Interview Feedback</CardTitle>
                <p className="text-xs text-blue-600/80">Log your weaknesses here. The AI will use this (via RAG) to give you better prep questions for your next applications.</p>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleAddFeedback} className="flex gap-2">
                  <Input 
                    value={feedback}
                    onChange={(e) => setFeedback(e.target.value)}
                    placeholder="e.g. I struggled with the system design question about caching..."
                    className="bg-white"
                  />
                  <Button type="submit" disabled={submittingFeedback || !feedback}>
                    <Send className="w-4 h-4 mr-2" />
                    Save
                  </Button>
                </form>
              </CardContent>
            </Card>

          </div>

        </div>
      </div>
    </div>
  );
}

function BriefcaseIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
      <rect width="20" height="14" x="2" y="6" rx="2" />
    </svg>
  )
}
