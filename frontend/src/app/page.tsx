"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Briefcase, Loader2, Plus } from "lucide-react";

type Job = {
  id: number;
  status: string;
  match_score: number | null;
  cover_letter: string | null;
  prep_questions: string[] | null;
};

const STATUS_COLUMNS = [
  { id: "ANALYZED", title: "Analyzed", statuses: ["PENDING", "COMPLETED", "FAILED"] },
  { id: "APPLIED", title: "Applied", statuses: ["APPLIED"] },
  { id: "INTERVIEWING", title: "Interviewing", statuses: ["INTERVIEWING"] },
  { id: "OFFER", title: "Offer", statuses: ["OFFER"] },
  { id: "REJECTED", title: "Rejected", statuses: ["REJECTED"] }
];

export default function Dashboard() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [url, setUrl] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const fetchJobs = async () => {
    try {
      const res = await fetch("http://localhost:8000/jobs");
      if (res.ok) {
        const data = await res.json();
        setJobs(data);
      }
    } catch (e) {
      console.error("Failed to fetch jobs", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJobs();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!url) return;
    
    setSubmitting(true);
    try {
      const res = await fetch("http://localhost:8000/jobs/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          cv_text: "Default Profile CV used.", // Hardcoded until Profile context is wired
          job_description: url
        })
      });
      if (res.ok) {
        setUrl("");
        fetchJobs(); // Refresh board
      }
    } catch (e) {
      console.error("Failed to submit job", e);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header & Input Bar */}
        <div className="flex flex-col md:flex-row justify-between items-center gap-4 bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-100 rounded-lg text-blue-600">
              <Briefcase size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Job Tracker</h1>
              <p className="text-sm text-gray-500">Manage your applications and ATS analysis</p>
            </div>
          </div>
          
          <form onSubmit={handleSubmit} className="flex w-full md:w-auto gap-2">
            <Input 
              placeholder="Paste LinkedIn/Glassdoor URL..." 
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full md:w-80"
              disabled={submitting}
            />
            <Button type="submit" disabled={submitting || !url}>
              {submitting ? <Loader2 className="animate-spin w-4 h-4 mr-2" /> : <Plus className="w-4 h-4 mr-2" />}
              Analyze
            </Button>
          </form>
        </div>

        {/* Kanban Board */}
        {loading ? (
          <div className="flex justify-center py-20">
            <Loader2 className="animate-spin text-gray-400 w-8 h-8" />
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-6 items-start">
            {STATUS_COLUMNS.map((col) => (
              <div key={col.id} className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <h2 className="font-semibold text-gray-700">{col.title}</h2>
                  <span className="bg-gray-200 text-gray-600 text-xs py-1 px-2 rounded-full font-medium">
                    {jobs.filter(j => col.statuses.includes(j.status)).length}
                  </span>
                </div>
                
                <div className="flex flex-col gap-3">
                  {jobs
                    .filter(j => col.statuses.includes(j.status))
                    .map(job => (
                      <Card key={job.id} className="shadow-sm cursor-pointer hover:shadow-md transition-shadow border-gray-200">
                        <CardHeader className="p-4 pb-2">
                          <CardTitle className="text-base text-gray-800">Job #{job.id}</CardTitle>
                        </CardHeader>
                        <CardContent className="p-4 pt-0">
                          <div className="flex items-center justify-between mt-2">
                            <span className={`text-xs px-2 py-1 rounded-md font-medium ${
                              job.status === 'COMPLETED' ? 'bg-green-100 text-green-700' :
                              job.status === 'FAILED' ? 'bg-red-100 text-red-700' :
                              job.status === 'PENDING' ? 'bg-yellow-100 text-yellow-700' :
                              'bg-gray-100 text-gray-700'
                            }`}>
                              {job.status}
                            </span>
                            {job.match_score !== null && (
                              <span className="text-sm font-bold text-blue-600">
                                {job.match_score}% Match
                              </span>
                            )}
                          </div>
                        </CardContent>
                      </Card>
                    ))}
                    
                  {jobs.filter(j => col.statuses.includes(j.status)).length === 0 && (
                    <div className="p-4 border-2 border-dashed border-gray-200 rounded-lg text-center text-sm text-gray-400">
                      No jobs
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
