import './Home.css'
// import UploadSection from './components/upload-section'
import PlayerSection from './components/player-section'
import Instruction from './components/instruction'
import VideoUpload from './components/video-upload'
import AppSidebar from './components/app-sidebar';
import Hero from './components/hero';
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
      <div className="flex w-full">
        <div className='w-[72px]'>
          <AppSidebar />
        </div>

        {/* Main content gets the remaining space */}
        <main className="flex-1 flex flex-col overflow-y-auto">
          <Hero />
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
