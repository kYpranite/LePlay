"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Upload, X } from "lucide-react"

export default function UploadSection() {
    const [file, setFile] = useState<File | null>(null)

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setFile(event.target.files[0])
        }
    }

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault()
        // Handle file upload logic here
        console.log("Uploading file:", file)
    }

    const handleCancel = () => {
        setFile(null)
    }

    

    return (
        <section className=" m-10 py-16 border-solid border-gray-200 border-2 w-11/12 rounded-2xl shadow-sm">
            <div className="container mx-auto px-4">
                {/* <h2 className="text-3xl font-bold mb-8 text-center text-gray-300 ">Upload Your NBA Game</h2> */}
                <form onSubmit={handleSubmit} className="max-w-md mx-auto">
                    <div className="mb-4">
                        <Label htmlFor="game-file" className="block text-center py-3">Upload your file here</Label>
                        <Input className="border-1 border-yellow-300 hover:border-sky-500" id="game-file" type="file" accept="video/*" onChange={handleFileChange} />
                    </div>
                    <Button type="submit" variant="secondary" className="w-full bg-yellow-500" disabled={!file}>
                        <Upload className="mr-2 h-4 w-4" /> Upload and Generate Highlights
                    </Button>
                    
                </form>
            </div>
        </section>
    )
}

