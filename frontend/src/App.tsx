
import './App.css'
import UploadSection from './components/upload-section'
import PlayerSection from './components/player-section'
import Instruction from './components/instruction'

export default function App() {

  return (
    <>
      <main className=' flex flex-col items-center py-4'>
        <UploadSection />
        <div className='w-full px-4 flex'>
          <PlayerSection />
          <Instruction />
        </div>


      </main>
    </>
  )
}

