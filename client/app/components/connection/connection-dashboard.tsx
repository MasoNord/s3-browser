import * as React from "react"
import { useParams, useSearchParams } from "react-router"
import { Folder, File, Download, Trash2, Upload, ArrowLeft } from "lucide-react"

import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "../ui/breadcrumb"

import { Separator } from "../ui/separator"
import { SidebarInset, SidebarProvider, SidebarTrigger } from "../ui/sidebar"

import { AppSidebar } from "./app-sidebar"
import { Button } from "../ui/button"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table"

import { readBucketObjects } from "~/api/objects/read"
import { s3BrowserAPIBaseV1 } from "~/api/config"

import { toast } from "sonner"

interface S3Folder {
  name: string
  full_key: string
}

interface S3File {
  name: string
  full_key: string
  size: number
  last_modified: string
}

interface BackendResponse {
  current_prefix: string
  folders: S3Folder[]
  files: S3File[]
}

export default function ConnectionDashboardPage() {
  const { connectionId } = useParams()
  const [searchParams, setSearchParams] = useSearchParams()

  const selectedBucket = searchParams.get("bucket")
  const currentPrefix = searchParams.get("prefix") || ""

  const [data, setData] = React.useState<BackendResponse | null>(null)
  const [loading, setLoading] = React.useState<boolean>(false)

  const fileInputRef = React.useRef<HTMLInputElement>(null)

  const fetchObjects = React.useCallback(async () => {
    if (!selectedBucket) return

    setLoading(true)

    try {
      const response = await readBucketObjects(
        connectionId!,
        selectedBucket,
        encodeURIComponent(currentPrefix)
      )

      const resData: BackendResponse = response.data

      setData(resData)
    } catch (err) {
      console.error("Ошибка загрузки данных S3:", err)
      toast.error("Ошибка загрузки объектов")
    } finally {
      setLoading(false)
    }
  }, [connectionId, selectedBucket, currentPrefix])

  React.useEffect(() => {
    fetchObjects()
  }, [fetchObjects])

  const handleSelectBucket = (bucketName: string) => {
    setSearchParams({
      bucket: bucketName,
      prefix: "",
    })

    setData(null)
  }

  const handleBreadcrumbClick = (index: number) => {
    if (!selectedBucket) return

    const parts = currentPrefix.split("/").filter(Boolean)

    if (index === -1) {
      setSearchParams({
        bucket: selectedBucket,
        prefix: "",
      })
    } else {
      const newPrefix = parts.slice(0, index + 1).join("/") + "/"

      setSearchParams({
        bucket: selectedBucket,
        prefix: newPrefix,
      })
    }
  }

  const handleGoBack = () => {
    if (!selectedBucket) return

    const parts = currentPrefix.split("/").filter(Boolean)

    if (parts.length <= 1) {
      setSearchParams({
        bucket: selectedBucket,
        prefix: "",
      })
    } else {
      const newPrefix = parts.slice(0, -1).join("/") + "/"

      setSearchParams({
        bucket: selectedBucket,
        prefix: newPrefix,
      })
    }
  }

  const handleDelete = async (key: string) => {
    if (!selectedBucket) return

    if (!window.confirm(`Вы уверены, что хотите удалить: ${key}?`)) {
      return
    }

    try {
      await s3BrowserAPIBaseV1.delete(`/objects/${connectionId}/delete`, {
        params: {
          bucket_name: selectedBucket,
          key: key,
          prefix: "",
        },
      })

      toast.success("Объект удалён")

      fetchObjects()
    } catch (error) {
      console.error(error)

      toast.error("Не удалось удалить объект")
    }
  }

  const handleDownload = async (key: string) => {
    if (!selectedBucket) return

    try {
      const response = await s3BrowserAPIBaseV1.post(
        `/objects/${connectionId}/download-url`,
        null,
        {
          params: {
            bucket_name: selectedBucket,
            key,
            prefix: "",
          },
        }
      )

      const downloadUrl = response.data?.url || response.data

      if (!downloadUrl) throw new Error("Empty URL")

      window.location.href = downloadUrl
    } catch (error) {
      console.error(error)
      toast.error("Ошибка получения ссылки")
    }
  }
  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]

    if (!file || !selectedBucket) return

    try {
      const formData = new FormData()

      formData.append("file", file)

      const result = await s3BrowserAPIBaseV1.post(
        `/objects/${connectionId}/upload`,
        formData,
        {
          params: {
            bucket_name: selectedBucket,
            prefix: currentPrefix,
          },
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      )

      if (
        result.status === 200 ||
        result.status === 201 ||
        result.status === 204
      ) {
        toast.success("Файл успешно загружен")

        fetchObjects()
      } else {
        console.error("Ошибка при загрузке файла")
      }
    } catch (error) {
      console.error(error)

      console.error("Ошибка при загрузке файла")
    } finally {
      if (fileInputRef.current) {
        fileInputRef.current.value = ""
      }
    }
  }

  const prefixParts = currentPrefix.split("/").filter(Boolean)

  return (
    <SidebarProvider>
      <AppSidebar
        selectedBucket={selectedBucket}
        onSelectBucket={handleSelectBucket}
      />

      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center justify-between gap-2 border-b pr-4">
          <div className="flex items-center gap-2 px-3">
            <SidebarTrigger />

            <Separator orientation="vertical" className="mr-2 h-4" />

            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink
                    href="#"
                    onClick={(e) => {
                      e.preventDefault()

                      handleBreadcrumbClick(-1)
                    }}
                  >
                    {selectedBucket || "Выберите бакет"}
                  </BreadcrumbLink>
                </BreadcrumbItem>

                {prefixParts.map((part, index) => (
                  <React.Fragment key={index}>
                    <BreadcrumbSeparator />

                    <BreadcrumbItem>
                      {index === prefixParts.length - 1 ? (
                        <BreadcrumbPage>{part}</BreadcrumbPage>
                      ) : (
                        <BreadcrumbLink
                          href="#"
                          onClick={(e) => {
                            e.preventDefault()

                            handleBreadcrumbClick(index)
                          }}
                        >
                          {part}
                        </BreadcrumbLink>
                      )}
                    </BreadcrumbItem>
                  </React.Fragment>
                ))}
              </BreadcrumbList>
            </Breadcrumb>
          </div>

          {selectedBucket && (
            <div>
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                onChange={handleFileUpload}
              />

              <Button
                size="sm"
                onClick={() => fileInputRef.current?.click()}
                className="gap-2"
              >
                <Upload className="size-4" />
                Upload File
              </Button>
            </div>
          )}
        </header>

        <div className="flex flex-1 flex-col gap-4 p-4">
          {!selectedBucket ? (
            <div className="flex flex-1 items-center justify-center rounded-xl border border-dashed text-muted-foreground">
              Выберите S3 бакет в левой панели для просмотра содержимого
            </div>
          ) : loading ? (
            <div className="flex flex-1 items-center justify-center text-muted-foreground">
              Загрузка объектов S3...
            </div>
          ) : (
            <div className="overflow-hidden rounded-xl border bg-card text-card-foreground shadow-sm">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Name</TableHead>

                    <TableHead className="w-[120px]">Size</TableHead>

                    <TableHead className="w-[200px]">Last Modified</TableHead>

                    <TableHead className="w-[100px] text-right">
                      Actions
                    </TableHead>
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {currentPrefix && (
                    <TableRow
                      className="cursor-pointer hover:bg-muted/40"
                      onClick={handleGoBack}
                    >
                      <TableCell className="flex items-center gap-2 font-medium text-blue-500">
                        <ArrowLeft className="size-4" />

                        <span>.. (Назад)</span>
                      </TableCell>

                      <TableCell>—</TableCell>

                      <TableCell>—</TableCell>

                      <TableCell />
                    </TableRow>
                  )}

                  {data?.folders.map((folder) => (
                    <TableRow
                      key={folder.full_key}
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() =>
                        setSearchParams({
                          bucket: selectedBucket,
                          prefix: folder.full_key,
                        })
                      }
                    >
                      <TableCell className="flex items-center gap-2 font-medium">
                        <Folder className="size-4 fill-amber-500/20 text-amber-500" />

                        <span>{folder.name}</span>
                      </TableCell>

                      <TableCell>—</TableCell>

                      <TableCell>—</TableCell>

                      <TableCell className="text-right">
                        <Button
                          size="icon"
                          variant="ghost"
                          className="h-8 w-8 text-destructive"
                          onClick={(e) => {
                            e.stopPropagation()

                            handleDelete(folder.full_key)
                          }}
                        >
                          <Trash2 className="size-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}

                  {data?.files.map((file) => (
                    <TableRow key={file.full_key} className="hover:bg-muted/30">
                      <TableCell className="flex items-center gap-2 font-medium">
                        <File className="size-4 text-slate-500" />

                        <span className="truncate" title={file.name}>
                          {file.name}
                        </span>
                      </TableCell>

                      <TableCell>
                        {file.size > 1024 * 1024
                          ? `${(file.size / (1024 * 1024)).toFixed(2)} MB`
                          : `${(file.size / 1024).toFixed(1)} KB`}
                      </TableCell>

                      <TableCell className="text-xs text-muted-foreground">
                        {new Date(file.last_modified).toLocaleString()}
                      </TableCell>

                      <TableCell className="text-right">
                        <div className="flex justify-end gap-1">
                          <Button
                            size="icon"
                            variant="ghost"
                            className="h-8 w-8 text-muted-foreground hover:text-foreground"
                            onClick={() => handleDownload(file.full_key)}
                          >
                            <Download className="size-4" />
                          </Button>

                          <Button
                            size="icon"
                            variant="ghost"
                            className="h-8 w-8 text-destructive"
                            onClick={() => handleDelete(file.full_key)}
                          >
                            <Trash2 className="size-4" />
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}

                  {(!data ||
                    (data.folders.length === 0 && data.files.length === 0)) && (
                    <TableRow>
                      <TableCell
                        colSpan={4}
                        className="py-8 text-center text-muted-foreground"
                      >
                        В этой папке пока нет файлов
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </div>
          )}
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
}
