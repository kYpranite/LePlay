import { Card, CardContent } from "@/components/ui/card"
import { Checkbox } from "@/components/ui/checkbox"

interface VideoClipProps {
  id: number
  src: string
  title: string
  onSelect: (id: number) => void
  isSelected: boolean
}

export default function VideoClip({ id, src, title, onSelect, isSelected }: VideoClipProps) {
  return (
    <Card className="overflow-hidden relative border-solid border-gray-200 border-2 w-full rounded-2xl shadow-sm">
      <CardContent className="p-0">
        <video
          className="w-full aspect-video object-cover"
          controls
          preload="auto"
        >
          <source src={src} type="video/mp4" />
          Your browser does not support the video tag.
        </video>
        <div className="p-4 flex justify-between items-center">
          <h2 className="text-lg font-semibold">{title}</h2>
          <Checkbox id={`select-clip-${id}`} checked={isSelected} onCheckedChange={() => onSelect(id)} />
        </div>
      </CardContent>
      {isSelected && <div className="absolute inset-0 bg-blue-200/20 pointer-events-none" />}
    </Card>
  )
}

