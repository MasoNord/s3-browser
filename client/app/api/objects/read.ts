import { s3BrowserAPIBaseV1 } from "../config"

export const readBucketObjects = async(connectionId: string,  bucketName: string, prefix: string) => {
    const response = await s3BrowserAPIBaseV1.get(`/objects/${connectionId}?bucket_name=${bucketName}&prefix=${prefix}`)

    return response
}