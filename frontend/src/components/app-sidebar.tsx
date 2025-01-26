"use client" // Remove this if not using Next.js at all

import { Layers, UserSquare2 } from "lucide-react"
import { Link, useLocation } from "react-router-dom"
import { cn } from "@/lib/utils"
import {
  Sidebar,
  SidebarContent,
  SidebarMenu,
  SidebarMenuItem,
  SidebarMenuButton,
} from "@/components/ui/sidebar"

const menuItems = [
  { icon: Layers, to: "/", label: "Home" },
  { icon: UserSquare2, to: "/clips", label: "Clips" },
]

export default function AppSidebar() {
  // useLocation replaces Next.js's usePathname
  const location = useLocation()
  const pathname = location.pathname

  return (
    <Sidebar collapsible="none" className="w-[60px] bg-[#1a1a1a] border-r-0">
      <SidebarContent className="py-4">
        <SidebarMenu>
          {menuItems.map((item) => (
            <SidebarMenuItem key={item.to}>
              <SidebarMenuButton asChild tooltip={item.label} className="w-full px-1">
                {/* Use `to` instead of `href` */}
                <Link
                  to={item.to}
                  className={cn(
                    "flex h-10 w-10 items-center justify-center rounded-lg mx-auto",
                    pathname === item.to
                      ? "bg-blue-600 text-white"
                      : "text-gray-400 hover:bg-gray-800 hover:text-gray-200"
                  )}
                >
                  <item.icon className="h-5 w-5" />
                  <span className="sr-only">{item.label}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
    </Sidebar>
  )
}
