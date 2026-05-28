import { ArrowRightFromLine, Check, Pencil, Plus, Trash, X } from "lucide-react"

import { useEffect, useState } from "react"
import { useNavigate } from "react-router"

import { s3BrowserAPIBaseV1 } from "~/api/config"

import { Button } from "../ui/button"
import { ButtonGroup } from "../ui/button-group"
import { Checkbox } from "../ui/checkbox"

import {
  Dialog,
  DialogClose,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "../ui/dialog"

import { Field, FieldDescription, FieldGroup, FieldLabel } from "../ui/field"

import { Input } from "../ui/input"
import { Label } from "../ui/label"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table"

type typeS3Connection = {
  id: string
  region_name: string
  endpoint_url: string
  aws_access_key_id: string
  aws_secret_access_key: string
  active?: boolean
}

type UpdateS3Setting = {
  region_name: string
  endpoint_url: string
  aws_access_key_id: string
  aws_secret_access_key: string
}

export default function ConnectionsPage() {
  const navigate = useNavigate()

  const [connections, setConnections] = useState<typeS3Connection[]>([])
  const [selectedConnection, setSelectedConnection] =
    useState<typeS3Connection | null>(null)

  const [isListOpen, setIsListOpen] = useState(false)
  const [isCreateOpen, setIsCreateOpen] = useState(false)
  const [isEditOpen, setIsEditOpen] = useState(false)
  const [isDeleteOpen, setIsDeleteOpen] = useState(false)

  const [formData, setFormData] = useState({
    region_name: "ru1",
    endpoint_url: "",
    aws_access_key_id: "",
    aws_secret_access_key: "",
  })

  const [editFormData, setEditFormData] = useState<UpdateS3Setting>({
    region_name: "",
    endpoint_url: "",
    aws_access_key_id: "",
    aws_secret_access_key: "",
  })

  const loadConnections = async () => {
    try {
      const [allRes, activeRes] = await Promise.all([
        s3BrowserAPIBaseV1.get<typeS3Connection[]>("/s3/settings/read-all"),

        s3BrowserAPIBaseV1.get<typeS3Connection[]>("/s3/connections/active"),
      ])

      const activeIds = new Set(activeRes.data.map((item) => item.id))

      const mappedConnections = allRes.data.map((conn) => ({
        ...conn,
        active: activeIds.has(conn.id),
      }))

      setConnections(mappedConnections)
    } catch (err) {
      console.error("Failed to fetch connections:", err)
    }
  }

  useEffect(() => {
    loadConnections()
  }, [])

  function connectionCheckout(connection: typeS3Connection, checked: boolean) {
    if (checked) {
      setSelectedConnection(connection)
    } else {
      setSelectedConnection(null)
    }
  }

  async function handleConnectSubmit() {
    if (!selectedConnection) return

    try {
      if (selectedConnection.active) {
        setIsListOpen(false)

        navigate(`/connection/${selectedConnection.id}/dashboard`)

        return
      }

      await s3BrowserAPIBaseV1.post(
        `/s3/connections/restore/${selectedConnection.id}`
      )

      setIsListOpen(false)

      navigate(`/connection/${selectedConnection.id}/dashboard`)
    } catch (err) {
      console.error("Failed to restore connection:", err)
    }
  }

  async function handleCreateAccount(e: React.FormEvent) {
    e.preventDefault()

    try {
      const response = await s3BrowserAPIBaseV1.post<typeS3Connection>(
        "/s3/connections",
        {
          region_name: formData.region_name,
          endpoint_url: formData.endpoint_url,
          aws_access_key_id: formData.aws_access_key_id,
          aws_secret_access_key: formData.aws_secret_access_key,
        }
      )

      setFormData({
        region_name: "ru1",
        endpoint_url: "",
        aws_access_key_id: "",
        aws_secret_access_key: "",
      })

      setIsCreateOpen(false)

      const newConnectionId = response.data.id

      navigate(`/connection/${newConnectionId}/dashboard`)
    } catch (err) {
      console.error("Failed to create new S3 credentials:", err)
    }
  }

  function handleOpenEdit() {
    if (!selectedConnection) return

    setEditFormData({
      region_name: selectedConnection.region_name,
      endpoint_url: selectedConnection.endpoint_url,
      aws_access_key_id: selectedConnection.aws_access_key_id,
      aws_secret_access_key: selectedConnection.aws_secret_access_key,
    })

    setIsEditOpen(true)
  }

  async function handleEditSubmit(e: React.FormEvent) {
    e.preventDefault()

    if (!selectedConnection) return

    try {
      const response = await s3BrowserAPIBaseV1.put(`/s3/settings/${selectedConnection.id}`, {
        region_name: editFormData.region_name,
        endpoint_url: editFormData.endpoint_url,
        aws_access_key_id: editFormData.aws_access_key_id,
        aws_secret_access_key: editFormData.aws_secret_access_key,
      })

      setIsEditOpen(false)

      selectedConnection.aws_access_key_id = response.data.aws_access_key_id
      selectedConnection.aws_secret_access_key = response.data.aws_secret_access_key
      selectedConnection.endpoint_url = response.data.endpoint_url
      selectedConnection.region_name = response.data.region_name

      await loadConnections()
    } catch (err) {
      console.error("Failed to update connection:", err)
    }
  }

  async function handleDeleteConnection() {
    if (!selectedConnection) return

    try {
      await s3BrowserAPIBaseV1.delete(`/s3/settings/${selectedConnection.id}`)

      setConnections((prev) =>
        prev.filter((conn) => conn.id !== selectedConnection.id)
      )

      setSelectedConnection(null)

      setIsDeleteOpen(false)
    } catch (err) {
      console.error("Failed to delete connection:", err)
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <p className="mb-10 text-3xl font-semibold tracking-tight">
        Create or choose <span className="text-primary">S3 Account</span>
      </p>

      <div className="flex flex-row gap-4">
        {/* CREATE */}

        <Dialog open={isCreateOpen} onOpenChange={setIsCreateOpen}>
          <DialogTrigger asChild>
            <Button className="h-24 w-24">
              <Plus className="size-12 stroke-1" />
            </Button>
          </DialogTrigger>

          <DialogContent className="sm:max-w-sm">
            <form onSubmit={handleCreateAccount}>
              <DialogHeader>
                <DialogTitle>Add New Account</DialogTitle>

                <DialogDescription>Enter new account details</DialogDescription>
              </DialogHeader>

              <FieldGroup className="my-4 space-y-4">
                <Field>
                  <Label htmlFor="endpoint-url">Endpoint URL</Label>

                  <Input
                    id="endpoint-url"
                    required
                    placeholder="https://s3.ru1.storage.beget.cloud"
                    value={formData.endpoint_url}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        endpoint_url: e.target.value,
                      })
                    }
                  />

                  <FieldDescription>
                    S3 API storage gateway endpoint
                  </FieldDescription>
                </Field>

                <Field>
                  <Label htmlFor="region-name">Region Name</Label>

                  <Input
                    id="region-name"
                    value={formData.region_name}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        region_name: e.target.value,
                      })
                    }
                  />
                </Field>

                <Field>
                  <FieldLabel htmlFor="access-key-id">Access Key ID</FieldLabel>

                  <Input
                    id="access-key-id"
                    required
                    value={formData.aws_access_key_id}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        aws_access_key_id: e.target.value,
                      })
                    }
                  />
                </Field>

                <Field>
                  <FieldLabel htmlFor="secret-key">
                    Secret Access Key
                  </FieldLabel>

                  <Input
                    id="secret-key"
                    type="password"
                    required
                    value={formData.aws_secret_access_key}
                    onChange={(e) =>
                      setFormData({
                        ...formData,
                        aws_secret_access_key: e.target.value,
                      })
                    }
                  />
                </Field>
              </FieldGroup>

              <DialogFooter>
                <DialogClose asChild>
                  <Button variant="outline" type="button">
                    Close
                  </Button>
                </DialogClose>

                <Button type="submit">Add account</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>

        {/* LIST */}

        {connections.length > 0 && (
          <Dialog open={isListOpen} onOpenChange={setIsListOpen}>
            <DialogTrigger asChild>
              <Button className="h-24 w-24" variant="outline">
                <ArrowRightFromLine className="size-12 stroke-1" />
              </Button>
            </DialogTrigger>

            <DialogContent className="sm:max-w-3xl">
              <DialogHeader>
                <DialogTitle>Storage Accounts</DialogTitle>

                <DialogDescription>
                  View and manage your storage accounts
                </DialogDescription>
              </DialogHeader>

              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[50px]" />

                    <TableHead className="w-[250px]">Access Key ID</TableHead>

                    <TableHead className="w-[300px]">Endpoint URL</TableHead>

                    <TableHead className="w-[100px]">Active</TableHead>
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {connections.map((pC) => (
                    <TableRow key={pC.id} className="hover:bg-muted/50">
                      <TableCell>
                        <Checkbox
                          checked={selectedConnection?.id === pC.id}
                          onCheckedChange={(checked: boolean) =>
                            connectionCheckout(pC, checked)
                          }
                        />
                      </TableCell>

                      <TableCell className="max-w-[250px] truncate font-medium">
                        {pC.aws_access_key_id}
                      </TableCell>

                      <TableCell className="max-w-[300px] truncate text-muted-foreground">
                        {pC.endpoint_url}
                      </TableCell>

                      <TableCell>
                        {pC.active ? (
                          <Check className="h-4 w-4 text-green-500" />
                        ) : (
                          <X className="h-4 w-4 text-red-500" />
                        )}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              <DialogFooter>
                <div className="flex w-full items-center justify-between">
                  <ButtonGroup className="gap-2">
                    <Button
                      variant="outline"
                      disabled={selectedConnection === null}
                      onClick={handleOpenEdit}
                    >
                      <Pencil className="mr-1 size-4" />
                      Edit
                    </Button>

                    <Button
                      variant="outline"
                      disabled={selectedConnection === null}
                      onClick={() => setIsDeleteOpen(true)}
                    >
                      <Trash className="mr-1 size-4" />
                      Delete
                    </Button>
                  </ButtonGroup>

                  <Button
                    disabled={selectedConnection === null}
                    onClick={handleConnectSubmit}
                  >
                    Connect
                  </Button>
                </div>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        )}

        {/* EDIT */}

        <Dialog open={isEditOpen} onOpenChange={setIsEditOpen}>
          <DialogContent className="sm:max-w-sm">
            <form onSubmit={handleEditSubmit}>
              <DialogHeader>
                <DialogTitle>Edit Account</DialogTitle>

                <DialogDescription>
                  Change storage account data
                </DialogDescription>
              </DialogHeader>

              <FieldGroup className="my-4 space-y-4">
                <Field>
                  <Label htmlFor="edit-endpoint">Endpoint URL</Label>

                  <Input
                    id="edit-endpoint"
                    required
                    value={editFormData.endpoint_url}
                    onChange={(e) =>
                      setEditFormData({
                        ...editFormData,
                        endpoint_url: e.target.value,
                      })
                    }
                  />
                </Field>

                <Field>
                  <Label htmlFor="edit-region">Region Name</Label>

                  <Input
                    id="edit-region"
                    value={editFormData.region_name}
                    onChange={(e) =>
                      setEditFormData({
                        ...editFormData,
                        region_name: e.target.value,
                      })
                    }
                  />
                </Field>

                <Field>
                  <Label htmlFor="edit-access">Access Key ID</Label>

                  <Input
                    id="edit-access"
                    required
                    value={editFormData.aws_access_key_id}
                    onChange={(e) =>
                      setEditFormData({
                        ...editFormData,
                        aws_access_key_id: e.target.value,
                      })
                    }
                  />
                </Field>

                <Field>
                  <Label htmlFor="edit-secret">Secret Access Key</Label>

                  <Input
                    id="edit-secret"
                    type="password"
                    required
                    value={editFormData.aws_secret_access_key}
                    onChange={(e) =>
                      setEditFormData({
                        ...editFormData,
                        aws_secret_access_key: e.target.value,
                      })
                    }
                  />
                </Field>
              </FieldGroup>

              <DialogFooter>
                <DialogClose asChild>
                  <Button variant="outline" type="button">
                    Cancel
                  </Button>
                </DialogClose>

                <Button type="submit">Save changes</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>

        {/* DELETE */}

        <Dialog open={isDeleteOpen} onOpenChange={setIsDeleteOpen}>
          <DialogContent className="sm:max-w-sm">
            <DialogHeader>
              <DialogTitle>Delete Connection</DialogTitle>

              <DialogDescription>
                Are you sure you want to delete this connection?
              </DialogDescription>
            </DialogHeader>

            <div className="rounded-md border p-3 text-sm">
              <p className="font-medium">
                {selectedConnection?.aws_access_key_id}
              </p>

              <p className="truncate text-muted-foreground">
                {selectedConnection?.endpoint_url}
              </p>
            </div>

            <DialogFooter>
              <DialogClose asChild>
                <Button variant="outline">Cancel</Button>
              </DialogClose>

              <Button variant="destructive" onClick={handleDeleteConnection}>
                Delete
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
