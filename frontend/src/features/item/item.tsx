import { ItemState } from './itemState'
import {
    Button,
    ButtonGroup,
    Card,
    CardHeader,
    CardActions,
    CardContent,
    CardMedia,
    Chip,
    FormControl,
    IconButton,
    InputLabel,
    MenuItem,
    Select,
    Typography
} from '@mui/material'
import DeleteIcon from '@mui/icons-material/Delete'
import EditIcon from '@mui/icons-material/Edit'

export const Item = ItemState => {
    return (
        <Card sx={{ maxWidth: 300, maxHeight: 800 }}>
            <CardHeader
                title={ItemState.name}
                action={
                    <ButtonGroup>
                        <IconButton>
                            <EditIcon />
                        </IconButton>
                        <IconButton>
                            <DeleteIcon />
                        </IconButton>
                    </ButtonGroup>
                }
            />
            <CardMedia
                component='img'
                height='194'
                image='https://via.placeholder.com/300x200'
                alt='Item Image'
            />
            <CardContent>
                <Typography variant='body2' color='text.secondary'>
                    {ItemState.description}
                </Typography>
                <Chip 
                    label={ItemState.status} 
                    color='primary'
                    size='small'
                />
                <Chip
                    label='Link'
                    component='a'
                    color='secondary'
                    href={ItemState.link}
                    size='small'
                    clickable
                />
                <Chip label='Tag' size='small'/>
                <Chip label='Tag' size='small'/>
                <Chip label='Tag' size='small'/>
            </CardContent>
            <CardActions disableSpacing></CardActions>
        </Card>
    )
}
