import { Button } from "./ui/button";

export default function UploadButton({ video }: { video: File | null }) {

    const handleClick = (e: React.MouseEvent) => {
        e.preventDefault()
        if (video) {
            // Here you would typically send the video to your server
            console.log("Uploading video:", video.name)
        } else {
            console.log("No video selected")
        }
    }
    return (
        <Button variant={"sky"} className="w-2/12" onClick={handleClick}>Upload</Button>
    )
}