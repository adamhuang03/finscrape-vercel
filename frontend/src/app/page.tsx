'use client';
import { Button } from "@/components/ui/button";
import { redirect } from "next/navigation"; // not for client side
import { useRouter } from "next/navigation";


export default function Home() {
  const router = useRouter();

  const handleRedirect = () => {
    router.push('/betakit-funding');
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-center p-24 gap-6">
      <div className="text-7xl flex space-x-4">
        <span className="fade-in word-1">Adam&apos;s</span>
        <span className="fade-in word-2">Humble</span>
        <span className="fade-in word-3">Abode</span>
      </div>
      <Button className="fade-in word-4" onClick={handleRedirect}>Betakit Fund Articles</Button>
    </div>
  );
}


