import { CommentState } from '../comment/commentState'

export type ItemState = {
    item_id: string
    name: string
    description: string
    link: string
    status: string
    comments: CommentState[]
}