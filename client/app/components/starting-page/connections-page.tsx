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
import { useState } from "react"
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

type typeS3Connection = {
  id: string
  name: string
  type: string
  active: boolean
}

const previouseConnections: typeS3Connection[] = [
  {
    id: "uuidv7-1",
    name: "Connections 1",
    type: "S3 Compatible Storage",
    active: true,
  },
  {
    id: "uuidv7-2",
    name: "Connections 3",
    type: "S3 Compatible Storage",
    active: false,
  },
]

const previouseConnectionsEmpty = []

export default function ConnectionsPage() {
  const [selectedConnection, setSelectedConnection] =
    useState<typeS3Connection | null>(null)

  function connectionCheckout(connection: typeS3Connection, checked: boolean) {
    if (checked) {
      setSelectedConnection(connection)
    } else {
      setSelectedConnection(null)
    }
  }

  function handlConnectSubmit() {
    console.log("Handle Connection Submit button pressed")
    window.location.href =`/connection/${selectedConnection?.id}/dashboard`
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center">
      <p className="mb-10 text-3xl font-semibold tracking-tight">
        Create or chooose <span className="text-primary">S3 Account</span>
      </p>
      <div className="flex flex-row gap-4">
        <Dialog>
          <form>
            <DialogTrigger asChild>
              <Button className="h-24 w-24">
                <Plus className="size-12 stroke-1" />
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-sm">
              <DialogHeader>
                <DialogTitle>Add New Account</DialogTitle>
                <DialogDescription>
                  Enter new account details and click "Add new account"
                </DialogDescription>
              </DialogHeader>
              <FieldGroup>
                <Field>
                  <Label htmlFor="display-name">Display name</Label>
                  <Input
                    id="display-name"
                    name="display-name"
                    placeholder="New Account"
                  ></Input>
                  <FieldDescription>
                    Assign any name to your account
                  </FieldDescription>
                </Field>
                <Field>
                  <FieldLabel htmlFor="account-key-id">
                    Access Key ID <span className="text-destructive">*</span>
                  </FieldLabel>
                  <Input
                    id="account-key-id"
                    name="account-key-id"
                    required
                  ></Input>
                  <FieldDescription>
                    Required to sign the requests you send to Amazon S3
                  </FieldDescription>
                </Field>
                <Field>
                  <FieldLabel htmlFor="secret-access-key">
                    Secret Access Key{" "}
                    <span className="text-destructive">*</span>
                  </FieldLabel>
                  <Input
                    id="secret-access-key"
                    name="secret-access-key"
                    required
                  ></Input>
                  <FieldDescription>
                    Required to sign the requests you send to Amazon S3
                  </FieldDescription>
                </Field>
              </FieldGroup>
              <DialogFooter>
                <DialogClose asChild>
                  <Button variant="outline">Close</Button>
                </DialogClose>
                <Button type="submit">Add new account</Button>
              </DialogFooter>
            </DialogContent>
          </form>
        </Dialog>

        {previouseConnections.length > 0 && (
          <Dialog>
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
                    <TableHead></TableHead>
                    <TableHead className="w-[200px]">Account Name</TableHead>
                    <TableHead className="w-[200px]">Account Type</TableHead>
                    <TableHead className="w-[200px]">Active</TableHead>
                  </TableRow>
                </TableHeader>

                <TableBody>
                  {previouseConnections.map((pC) => (
                    <TableRow key={pC.id} className="hover:bg-muted/50">
                      <TableCell>
                        <Checkbox
                          onCheckedChange={(checked: boolean) =>
                            connectionCheckout(pC, checked)
                          }
                          checked={selectedConnection?.id === pC.id}
                        />
                      </TableCell>
                      <TableCell className="text-black-500 font-medium">
                        {pC.name}
                      </TableCell>
                      <TableCell className="text-black-500 font-medium">
                        {pC.type}
                      </TableCell>
                      <TableCell className="text-black-500 font-medium">
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
                <div className="flex w-full">
                  <ButtonGroup className="flex w-full justify-start">
                    <Button
                      variant="outline"
                      disabled={selectedConnection != null ? false : true}
                    >
                      {" "}
                      <Pencil /> Edit
                    </Button>
                    <Button
                      variant="outline"
                      disabled={selectedConnection != null ? false : true}
                    >
                      {" "}
                      <Trash /> Delete
                    </Button>
                  </ButtonGroup>

                  <ButtonGroup>
                    <Button
                      disabled={selectedConnection != null ? false : true}
                      onClick={() => handlConnectSubmit()}
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
