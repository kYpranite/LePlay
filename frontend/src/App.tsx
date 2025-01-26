import './App.css'
// import UploadSection from './components/upload-section'
import PlayerSection from './components/player-section'
import Instruction from './components/instruction'
import VideoUpload from './components/video-upload'
import SidebarBlack from './components/sidebar-black';
import { SidebarProvider } from './components/ui/sidebar';
import { useState } from 'react';


export default function App() {
  const [players, setPlayers] = useState<string[]>([])
  const [instruction, setInstruction] = useState<string>("")

  const handleAddPlayer = (player: string) => {
    setPlayers([...players, player])
    console.log("Added player:", player)
  }

  const handleRemovePlayer = (index: number) => {
    setPlayers(players.filter((_, i) => i !== index))
  }

  const handleAddInstruction = (instruction: string) => {
    setInstruction(instruction)
    console.log(instruction)
  }


  return (
    <SidebarProvider>
      {/* Use a flex container for the entire layout */}
      <div className="flex w-11/12 ml-10">
        {/* The sidebar can have a fixed or min-width to avoid overlap */}
        <div className="mr-7">
          <SidebarBlack />
        </div>

        {/* Main content gets the remaining space */}
        <main className="flex-1 flex flex-col py-2 w-">
          <VideoUpload instruction={instruction} players={players} />
          <div className="w-full px-4 flex m-0">
            <PlayerSection handleAddPlayer={handleAddPlayer} handleRemovePlayer={handleRemovePlayer} />
            <Instruction handleAddInstruction={handleAddInstruction} />
          </div>
        </main>
      </div>
    </SidebarProvider>
  )
}
