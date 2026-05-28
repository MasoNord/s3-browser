import * as React from "react"
import { Box, FolderIcon, Plus, Pencil } from "lucide-react"
import { useParams } from "react-router"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "../ui/sidebar"
import { Button } from "../ui/button"
import { readAllBuckets } from "~/api/buckets/read"
import type { ReadBucket } from "~/api/buckets/responses"

interface AppSidebarProps extends React.ComponentProps<typeof Sidebar> {
  selectedBucket: string | null;
  onSelectBucket: (bucket: string) => void;
}

export function AppSidebar({ selectedBucket, onSelectBucket, ...props }: AppSidebarProps) {
  const { connectionId } = useParams()
  const [buckets, setBuckets] = React.useState<ReadBucket[]>([])
  const [loading, setLoading] = React.useState(true)

  async function loadBuckets(connectionId: string | undefined) {
    const data = await readAllBuckets(connectionId)
    setBuckets(data)
    setLoading(false)
  }

  React.useEffect(() => {
    loadBuckets(connectionId)
  }, [connectionId])

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                  <Box className="size-4" />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-medium">S3 Explorer</span>
                  <span className="text-xs text-muted-foreground">v1.0.0</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <span className="px-4 text-xs font-semibold text-muted-foreground uppercase tracking-wider">
            Buckets
          </span>
          <SidebarMenu className="mt-2">
            {loading ? (
              <p className="px-4 text-sm text-muted-foreground">Loading...</p>
            ) : buckets.length === 0 ? (
              <p className="px-4 text-sm text-muted-foreground">No buckets found</p>
            ) : (
              buckets.map((bucket) => (
                <SidebarMenuItem key={bucket.name}>
                  <SidebarMenuButton 
                    isActive={selectedBucket === bucket.name}
                    onClick={() => onSelectBucket(bucket.name)}
                    className="w-full justify-start gap-2"
                  >
                    <FolderIcon className="size-4 text-amber-500 fill-amber-500/20" />
                    <span className="truncate">{bucket.name}</span>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))
            )}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
      <SidebarFooter>
        <div className="flex w-full justify-between gap-2 p-2">
          <Button variant="outline" className="flex-1 text-xs"><Plus className="size-3 mr-1"/> Add</Button>
          <Button variant="outline" className="flex-1 text-xs"><Pencil className="size-3 mr-1"/> Edit</Button>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}