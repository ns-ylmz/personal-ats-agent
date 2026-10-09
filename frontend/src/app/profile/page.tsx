"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardContent, CardDescription } from "@/components/ui/card";
import { ArrowLeft, Upload, Loader2, FileText, Briefcase } from "lucide-react";

type ProfileData = {
  skills: string[];
  experience_summary: string;
};

export default function ProfilePage() {
  const router = useRouter();
  const [profile, setProfile] = useState<ProfileData | null>(null);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  const fetchProfile = async () => {
    try {
      const res = await fetch("http://localhost:8000/profile");
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
      }
    } catch (e) {
      console.error("Failed to fetch profile", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://localhost:8000/profile/upload", {
        method: "POST",
        body: formData,
      });
      if (res.ok) {
        const data = await res.json();
        setProfile({
          skills: data.skills,
          experience_summary: data.experience_summary
        });
        setFile(null);
      } else {
        alert("Upload failed. Ensure backend is running and LLM is accessible.");
      }
    } catch (e) {
      console.error("Upload error", e);
      alert("Error uploading file.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 md:p-12">
      <div className="max-w-4xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Button variant="outline" size="icon" onClick={() => router.push("/")}>
            <ArrowLeft className="w-4 h-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold text-gray-900">My Master Profile</h1>
            <p className="text-sm text-gray-500">Upload your CV to extract your skills and experience context.</p>
          </div>
        </div>

        {/* Upload Section */}
        <Card className="border-dashed border-2 border-blue-200 bg-blue-50/30">
          <CardHeader>
            <CardTitle className="text-lg flex items-center gap-2 text-blue-800">
              <Upload className="w-5 h-5" />
              Upload New CV (PDF)
            </CardTitle>
          </CardHeader>
          <CardContent className="flex items-center gap-4">
            <input 
              type="file" 
              accept=".pdf" 
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="text-sm text-gray-600 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            />
            <Button onClick={handleUpload} disabled={!file || uploading}>
              {uploading ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : "Extract & Save Profile"}
            </Button>
          </CardContent>
        </Card>

        {/* Profile Display Section */}
        {loading ? (
          <div className="flex justify-center p-12">
            <Loader2 className="w-8 h-8 animate-spin text-gray-400" />
          </div>
        ) : profile ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <FileText className="w-5 h-5 text-green-600" />
                  Extracted Skills
                </CardTitle>
                <CardDescription>Key competencies identified by the AI</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {profile.skills.map((skill, idx) => (
                    <span key={idx} className="bg-green-100 text-green-800 text-xs font-medium px-2.5 py-0.5 rounded border border-green-200">
                      {skill}
                    </span>
                  ))}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Briefcase className="w-5 h-5 text-purple-600" />
                  Experience Summary
                </CardTitle>
                <CardDescription>AI-generated professional summary</CardDescription>
              </CardHeader>
              <CardContent>
                <p className="text-sm text-gray-700 leading-relaxed">
                  {profile.experience_summary}
                </p>
              </CardContent>
            </Card>
          </div>
        ) : (
          <div className="text-center p-12 bg-white rounded-xl border border-gray-200 shadow-sm">
            <h3 className="text-lg font-medium text-gray-900">No profile found</h3>
            <p className="text-sm text-gray-500 mt-1">Upload a PDF CV above to get started.</p>
          </div>
        )}

      </div>
    </div>
  );
}
