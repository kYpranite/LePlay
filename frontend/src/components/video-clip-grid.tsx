import VideoClip from "./video-clip"
import { useState, useEffect } from 'react';
import { Button } from "./ui/button";
import axios from "axios"

// This would typically come from an API or database


interface VideoClipGridProps {
  onClipSelect: (id: number) => void
  selectedClips: number[]
}

export default function VideoClipGrid({ onClipSelect, selectedClips }: VideoClipGridProps) {

  interface VideoClipProp {
    id: number;
    src: string;
    title: string;
  }


  const [videoClips, setVideoClips] = useState<VideoClipProp[]>([])
  const fetchVideoClips = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5050/api/data")
      setVideoClips(response.data)
      console.log(response.data)
    } catch (error) {
      console.error("Error fetching video clips:", error)
    }
  }
  const handleDownloadSelected = async () => {
    // Filter the clips that are currently selected
    const clipsToDownload = videoClips.filter((clip) =>
      selectedClips.includes(clip.id)
    )

    for (const clip of clipsToDownload) {
      try {
        const response = await fetch(clip.src)
        const blob = await response.blob()
        const url = URL.createObjectURL(blob)

        const link = document.createElement("a")
        link.href = url
        // Use clip.title or a fallback name for the download filename
        link.download = clip.title ? `${clip.title}.mp4` : `video-${clip.id}.mp4`
        document.body.appendChild(link)
        link.click()
        URL.revokeObjectURL(url)
      } catch (err) {
        console.error(`Failed to download ${clip.title}:`, err)
      }
    }
  }

  useEffect(() => {
    fetchVideoClips()
  }, [])

  return (
    <div className="flex flex-col justify-end">
      <Button variant={"customBlack"} className="w-2/12" onClick={handleDownloadSelected}>Download Selected</Button>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 overflow-hidden relative border-solid border-gray-200 border-2 w-full rounded-2xl shadow-md p-10 my-3">
        {videoClips.map((clip) => (
          <VideoClip
            key={clip.id}
            id={clip.id}
            src={clip.src}
            title={clip.title}
            onSelect={onClipSelect}
            isSelected={selectedClips.includes(clip.id)}
          />
        ))}
      </div>
    </div>

  )
}

