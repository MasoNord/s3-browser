import { ArrowRightFromLine, Check, Pencil, Plus, Trash, X } from "lucide-react"
import { Button } from "../ui/button"
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
import { Label } from "../ui/label"
import { Input } from "../ui/input"
import { useState, useEffect } from "react"
import { useNavigate } from "react-router"
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "../ui/table"
import { ButtonGroup } from "../ui/button-group"
import { Checkbox } from "../ui/checkbox"
import { s3BrowserAPIBaseV1 } from "~/api/config"

type typeS3Connection = {
  id: string
  region_name: string
  endpoint_url: string
  aws_access_key_id: string
  aws_secret_access_key: string
  active?: boolean
}

export default function ConnectionsPage() {
  const navigate = useNavigate()
  const [connections, setConnections] = useState<typeS3Connection[]>([])
  const [selectedConnection, setSelectedConnection] = useState<typeS3Connection | null>(null)
  const [isListOpen, setIsListOpen] = useState(false)
  const [isCreateOpen, setIsCreateOpen] = useState(false)

  const [formData, setFormData] = useState({
    region_name: "ru1",
    endpoint_url: "",
    aws_access_key_id: "",
    aws_secret_access_key: ""
  })

  const loadConnections = async () => {
    try {
      const [allRes, activeRes] = await Promise.all([
        s3BrowserAPIBaseV1.get<typeS3Connection[]>("/s3/settings/read-all"),
        s3BrowserAPIBaseV1.get<typeS3Connection[]>("/s3/connections/active")
      ])

      const activeIds = new Set(activeRes.data.map(item => item.id))
      
      const mappedConnections = allRes.data.map(conn => ({
        ...conn,
        active: activeIds.has(conn.id)
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

      await s3BrowserAPIBaseV1.post(`/s3/connections/restore/${selectedConnection.id}`)
      
      setIsListOpen(false)
      navigate(`/connection/${selectedConnection.id}/dashboard`)
    } catch (err) {
      console.error("Failed to restore connection:", err)
    }
  }

  async function handleCreateAccount(e: React.FormEvent) {
    e.preventDefault()
    try {
      const response = await s3BrowserAPIBaseV1.post<typeS3Connection>("/s3/connections", {
        region_name: formData.region_name,
        endpoint_url: formData.endpoint_url,
        aws_access_key_id: formData.aws_access_key_id,
        aws_secret_access_key: formData.aws_secret_access_key
      })

      setFormData({
        region_name: "ru1",
        endpoint_url: "",
        aws_access_key_id: "",
        aws_secret_access_key: ""
      })
      
      setIsCreateOpen(false)
      
      const newConnectionId = response.data.id
      navigate(`/connection/${newConnectionId}/dashboard`)
    } catch (err) {
      console.error("Failed to create new S3 credentials:", err)
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <p className="mb-10 text-3xl font-semibold tracking-tight">
        Create or choose <span className="text-primary">S3 Account</span>
      </p>
      <div className="flex flex-row gap-4">
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
                <DialogDescription>
                  Enter new account details and click "Add new account"
                </DialogDescription>
              </DialogHeader>
              <FieldGroup className="space-y-4 my-4">
                <Field>
                  <Label htmlFor="endpoint-url">Endpoint URL <span className="text-destructive">*</span></Label>
                  <Input
                    id="endpoint-url"
                    name="endpoint-url"
                    required
                    placeholder="https://s3.ru1.storage.beget.cloud"
                    value={formData.endpoint_url}
                    onChange={(e) => setFormData({ ...formData, endpoint_url: e.target.value })}
                  />
                  <FieldDescription>
                    S3 API storage gateway endpoint link
                  </FieldDescription>
                </Field>
                <Field>
                  <Label htmlFor="region-name">Region name</Label>
                  <Input
                    id="region-name"
                    name="region-name"
                    placeholder="ru1"
                    value={formData.region_name}
                    onChange={(e) => setFormData({ ...formData, region_name: e.target.value })}
                  />
                </Field>
                <Field>
                  <FieldLabel htmlFor="account-key-id">
                    Access Key ID <span className="text-destructive">*</span>
                  </FieldLabel>
                  <Input
                    id="account-key-id"
                    name="account-key-id"
                    required
                    value={formData.aws_access_key_id}
                    onChange={(e) => setFormData({ ...formData, aws_access_key_id: e.target.value })}
                  />
                </Field>
                <Field>
                  <FieldLabel htmlFor="secret-access-key">
                    Secret Access Key <span className="text-destructive">*</span>
                  </FieldLabel>
                  <Input
                    id="secret-access-key"
                    name="secret-access-key"
                    required
                    type="password"
                    value={formData.aws_secret_access_key}
                    onChange={(e) => setFormData({ ...formData, aws_secret_access_key: e.target.value })}
                  />
                </Field>
              </FieldGroup>
              <DialogFooter>
                <DialogClose asChild>
                  <Button variant="outline" type="button">Close</Button>
                </DialogClose>
                <Button type="submit">Add new account</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>

        {connections.length > 0 && (
          <Dialog open={isListOpen} onOpenChange={setIsListOpen}>
            <DialogTrigger asChild>
              <Button
                title="Открыть предыдущие соединения"
                className="h-24 w-24"
                variant="outline"
              >
                <ArrowRightFromLine className="size-12 stroke-1" />
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-3xl">
              <DialogHeader>
                <DialogTitle>Storage Accounts</DialogTitle>
                <DialogDescription>
                  View, add, edit and delete your storage accounts
                </DialogDescription>
              </DialogHeader>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-[50px]"></TableHead>
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
                          onCheckedChange={(checked: boolean) =>
                            connectionCheckout(pC, checked)
                          }
                          checked={selectedConnection?.id === pC.id}
                        />
                      </TableCell>
                      <TableCell className="font-medium truncate max-w-[250px]">
                        {pC.aws_access_key_id}
                      </TableCell>
                      <TableCell className="font-medium text-muted-foreground truncate max-w-[300px]">
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
                <div className="flex w-full justify-between items-center">
                  <ButtonGroup className="flex justify-start gap-2">
                    <Button
                      variant="outline"
                      type="button"
                      disabled={selectedConnection === null}
                    >
                      <Pencil className="size-4 mr-1" /> Edit
                    </Button>
                    <Button
                      variant="outline"
                      type="button"
                      disabled={selectedConnection === null}
                    >
                      <Trash className="size-4 mr-1" /> Delete
                    </Button>
                  </ButtonGroup>

                  <ButtonGroup>
                    <Button
                      type="button"
                      disabled={selectedConnection === null}
                      onClick={handleConnectSubmit}
                    >
                      Connect
                    </Button>
                  </ButtonGroup>
                </div>
              </DialogFooter>
            </DialogContent>
          </Dialog>
        )}
      </div>
    </div>
  )
}