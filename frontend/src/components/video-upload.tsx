"use client"

import { useState, useCallback } from "react"
import { useDropzone } from "react-dropzone"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Upload, X } from "lucide-react"
import axios from "axios"
import { useNavigate } from "react-router-dom"


export default function VideoUpload({ instruction, players }: { instruction: string, players: string[] }) {
    const navigate = useNavigate()
    const [video, setVideo] = useState<File | null>(null)
    const [previewUrl, setPreviewUrl] = useState<string | null>(null)
    const [clicked, setClicked] = useState(false)

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const file = acceptedFiles[0]
        console.log(file)
        if (file && file.type.startsWith("video/")) {
            setVideo(file)
            setPreviewUrl(URL.createObjectURL(file))
        }
    }, [])

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { "video/mp4": [] },
        multiple: false,
    })

    const handleUpload = async () => {
        const formData = new FormData()
        setClicked(true)
        if (video) {
            // Here you would typically send the video to your server
            formData.append("video", video)
            formData.append("instruction", instruction)
            formData.append("players", JSON.stringify(players))

            try {

                const response = await axios.post("http://127.0.0.1:5000/api/upload", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                })
                if (response.status === 200) {
                    console.log("Video uploaded successfully")
                    navigate("/clips")

                }
            } catch (error) {
                console.error("Error uploading video:", error)
            }
        }
    }

    const handleClear = () => {
        setVideo(null)
        setPreviewUrl(null)
    }

    return (
        <Card className="w-full">
            <CardHeader>
                <CardTitle>Upload Video</CardTitle>
            </CardHeader>
            <CardContent>
                <div
                    {...getRootProps()}
                    className={`border-2 w-full border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${isDragActive ? "border-primary bg-primary/10" : "border-gray-300 hover:border-primary"
                        }`}
                >
                    <input {...getInputProps()} />
                    {previewUrl ? (
                        <div className="w-2/9 mx-auto flex justify-center">
                            <video src={previewUrl} controls className="w-full h-full object-contain">
                            </video>
                        </div>
                    ) : (
                        <div className="flex flex-col items-center">
                            <Upload className="h-12 w-12 text-gray-400 mb-4" />
                            <p className="text-lg font-semibold mb-2">
                                {isDragActive ? "Drop the video here" : "Drag & drop video here"}
                            </p>
                            <p className="text-sm text-gray-500">or click to select</p>
                        </div>
                    )}
                </div>
                {video && (
                    <div className="mt-4 text-sm text-muted-foreground">
                        <p>File: {video.name}</p>
                        <p>Size: {(video.size / 1024 / 1024).toFixed(2)} MB</p>
                    </div>
                )}
            </CardContent>
            <CardFooter className="flex justify-end space-x-2 mx-0">
                {video && (
                    <>
                        <Button onClick={handleClear}>
                            <X className="h-4 w-4 mr-2" />
                            Clear
                        </Button>
                        <Button onClick={handleUpload} variant={"customBlack"} disabled={clicked}>
                            <Upload className="h-4 w-4 mr-2" />
                            Upload
                        </Button>
                    </>
                )}
            </CardFooter>
        </Card>
    )
}

