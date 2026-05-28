import { s3BrowserAPIBaseV1 } from "../config"
import type { ReadBucket } from "./responses"



export const readAllBuckets = async(connectionId: string | undefined): Promise<ReadBucket[]> => {
    const response =  await s3BrowserAPIBaseV1.get<ReadBucket[]>(`/buckets/${connectionId}`)

    return response.data
}