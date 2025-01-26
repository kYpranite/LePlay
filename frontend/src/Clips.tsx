"use client"

import { useState } from "react"
import VideoClipGrid from "./components/video-clip-grid"
import AppSidebar from "./components/app-sidebar"
import { Sidebar } from "lucide-react"
import { SidebarProvider } from "./components/ui/sidebar"

export default function Clips() {
    const [selectedClips, setSelectedClips] = useState<number[]>([])

    const handleClipSelect = (id: number) => {
        setSelectedClips((prev) => (prev.includes(id) ? prev.filter((clipId) => clipId !== id) : [...prev, id]))
    }



    return (
        <SidebarProvider>
            <div>
                <AppSidebar />
            </div>

            <div className="container mx-auto px-4 py-8">
                <h1 className="text-3xl font-bold mb-6">Clips Gallery</h1>
                <div className="mb-4">
                    <span className="text-lg font-semibold">
                        {selectedClips.length} clip{selectedClips.length !== 1 ? "s" : ""} selected
                    </span>
                </div>
                <VideoClipGrid onClipSelect={handleClipSelect} selectedClips={selectedClips} />
            </div>
        </SidebarProvider>

    )
}

