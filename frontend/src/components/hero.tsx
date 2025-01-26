import { Link } from "react-router-dom"
import { Play } from "lucide-react"
import { Button } from "@/components/ui/button"
import heroCover from "../assets/hero_cover.mp4"

export default function Hero() {
    return (
        <section className="relative bg-[#1a1a1a] text-white overflow-hidden w-full">
            {/* Background Video */}
            <div className="absolute inset-0 w-full h-full">
                <video autoPlay loop muted className="w-full h-full object-cover opacity-50">
                    <source src={heroCover} type="video/mp4" />
                </video>
            </div>

            {/* Content */}
            <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32 ">
                <div className="text-center">
                    <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-4">
                        LePlay
                    </h1>
                    <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
                        Never miss a moment. Generate the best highlights from your favorite
                        games.
                    </p>
                    {/* Replace href with to using React Router */}
                    <Link to="/highlights">
                        <Button size="lg" className="group">
                            <span>Watch Highlights</span>
                            <Play className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                        </Button>
                    </Link>
                </div>

                {/* Feature Highlights */}
                <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
                    {["Real-time Processing", "Multiple Games", "Customizable Feeds"].map((feature, index) => (
                        <div key={index} className="bg-white/10 backdrop-blur-sm rounded-lg p-6">
                            <h3 className="text-xl font-semibold mb-2">{feature}</h3>
                            <p className="text-gray-300">
                                Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                            </p>
                        </div>
                    ))}
                </div>
            </div>

            {/* Scroll Indicator */}
            <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 animate-bounce">
                <svg
                    className="w-6 h-6"
                    fill="none"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                >
                    <path d="M19 14l-7 7m0 0l-7-7m7 7V3"></path>
                </svg>
            </div>
        </section>
    )
}
