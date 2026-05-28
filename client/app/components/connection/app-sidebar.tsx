import * as React from "react"
import { Box, FolderIcon, Plus, Pencil, LogOut } from "lucide-react"
import { useParams, useNavigate } from "react-router"
import { Check } from "lucide-react"

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
import { Popover, PopoverContent, PopoverTrigger } from "../ui/popover"
import { s3BrowserAPIBaseV1 } from "~/api/config"
import { toast } from "sonner"

interface AppSidebarProps extends React.ComponentProps<typeof Sidebar> {
  selectedBucket: string | null
  onSelectBucket: (bucket: string) => void
}

export function AppSidebar({
  selectedBucket,
  onSelectBucket,
  ...props
}: AppSidebarProps) {
  const { connectionId } = useParams()
  const navigate = useNavigate()
  const [bucketName, setBucketName] = React.useState("")
  const [selecting, setSelecting] = React.useState(false)
  const [buckets, setBuckets] = React.useState<ReadBucket[]>([])
  const [loading, setLoading] = React.useState(true)

  async function loadBuckets(connectionId: string | undefined) {
    const data = await readAllBuckets(connectionId)
    setBuckets(data)
    setLoading(false)
  }

  const handleCreate = async (bucketName: string) => {
    await s3BrowserAPIBaseV1.post(`/buckets/${connectionId}`, {
      name: bucketName,
    })

    toast.success("Bucket has been created successfully")
  }

  const handleSelect = async (bucketName: string) => {
    if (selecting) return
    if (bucketName === selectedBucket) return

    setSelecting(true)
    try {
      onSelectBucket(bucketName)
    } finally {
      setTimeout(() => setSelecting(false), 150)
    }
  }

  React.useEffect(() => {
    loadBuckets(connectionId)
  }, [connectionId])

  const currentBucket = selectedBucket
    ? buckets.find((b) => b.name === selectedBucket)
    : null

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
          <span className="px-4 text-xs font-semibold tracking-wider text-muted-foreground uppercase">
            Buckets
          </span>

          <SidebarMenu className="mt-2">
            {loading ? (
              <p className="px-4 text-sm text-muted-foreground">Loading...</p>
            ) : buckets.length === 0 ? (
              <p className="px-4 text-sm text-muted-foreground">
                No buckets found
              </p>
            ) : (
              buckets.map((bucket) => (
                <SidebarMenuItem key={bucket.name}>
                  <SidebarMenuButton
                    isActive={selectedBucket === bucket.name}
                    onClick={() => handleSelect(bucket.name)}
                    className="w-full justify-between gap-2"
                    disabled={selecting}
                  >
                    <div className="flex min-w-0 items-center gap-2">
                      <FolderIcon className="size-4 shrink-0 fill-amber-500/20 text-amber-500" />
                      <span className="truncate">{bucket.name}</span>
                    </div>

                    {selectedBucket === bucket.name && (
                      <Check className="size-4 shrink-0 text-green-500" />
                    )}
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))
            )}
          </SidebarMenu>
        </SidebarGroup>
      </SidebarContent>

      <SidebarRail />

      <SidebarFooter>
        <div className="flex flex-col gap-2 p-2">
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="outline" className="w-full text-xs">
                <Plus className="mr-1 size-3" />
                Add
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-64">
              <div className="mb-2 text-sm font-medium">Create bucket</div>

              <input
                id="bucket-name"
                value={bucketName}
                onChange={(e) => setBucketName(e.target.value)}
                className="w-full rounded border px-2 py-1 text-sm"
                placeholder="Bucket name"
              />

              <Button onClick={() => handleCreate(bucketName)} className="mt-2 w-full text-xs">
                Create
              </Button>
            </PopoverContent>
          </Popover>

          <Popover>
            <PopoverContent className="w-64">
              <div className="mb-2 text-sm font-medium">Edit bucket</div>

              <input
                className="w-full rounded border px-2 py-1 text-sm"
                value={selectedBucket ?? ""}
                readOnly
              />

              <Button className="mt-2 w-full text-xs">Save</Button>
            </PopoverContent>
          </Popover>

          <Button
            variant="destructive"
            className="w-full text-xs"
            onClick={() => navigate("/")}
          >
            <LogOut className="mr-1 size-3" />
            Exit
          </Button>
        </div>
      </SidebarFooter>
    </Sidebar>
  )
}
