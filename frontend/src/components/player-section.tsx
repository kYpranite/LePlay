"use client"

import { useState } from "react"
import { Plus, X } from "lucide-react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"



export default function PlayerSection({ handleAddPlayer, handleRemovePlayer }: { handleAddPlayer: (player: string) => void, handleRemovePlayer: (index: number) => void }) {
  const [inputText, setInputText] = useState("")
  const [items, setItems] = useState<string[]>([])

  const handleAddItem = () => {
    if (inputText.trim() !== "") {
      setItems([...items, inputText.trim()])
      handleAddPlayer(inputText.trim())
      setInputText("")
    }
  }

  const handleRemoveItem = (index: number) => {
    setItems(items.filter((_, i) => i !== index))
    handleRemovePlayer(index)
  }

  return (
    <Card className="m-10 border-solid border-gray-200 border-2 w-3/6 rounded-2xl shadow-sm">
      <CardHeader>
        <CardTitle>Players</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <Textarea
          placeholder="Enter your text here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          className="h-[0px]"
        />
        <Button onClick={handleAddItem} className="w-full" variant={"sky"}>
          <Plus className="mr-2 h-4 w-4" /> Add to List
        </Button>
        {items.length > 0 && (
          <ul className="list-disc list-inside space-y-2">
            {items.map((item, index) => (
              <li key={index} className="flex justify-between items-center text-md">
                {item}
                <button 
                  onClick={() => handleRemoveItem(index)} 
                  className="text-red-500 hover:text-red-700 ml-2"
                >
                  <X className="h-4 w-4" />
                </button>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  )
}

