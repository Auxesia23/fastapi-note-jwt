import io
from fastapi import APIRouter, Response, status, HTTPException, Depends
import pandas as pd
from app.models import  User_Pydantic, Note, Note_Pydantic, NoteIn_Pydantic
from app.auth import get_current_user

router = APIRouter(
    tags=['Note']
)

@router.get('/note', response_model=list[Note_Pydantic])
async def get_notes_by_user(user: User_Pydantic = Depends(get_current_user)):  # type: ignore
    notes_queryset = Note.filter(author_id=user.id)
    return await Note_Pydantic.from_queryset(notes_queryset)

@router.post('/note/add', response_model=Note_Pydantic)
async def note(note : NoteIn_Pydantic, user : User_Pydantic = Depends(get_current_user) ) : # type: ignore
    note_obj =  Note(title=note.title, body=note.body, author_id=user.id)
    await note_obj.save()
    return await Note_Pydantic.from_tortoise_orm(note_obj)


@router.get('/note/{note_id}', response_model=Note_Pydantic)
async def get_note_by_id(note_id: int, user: User_Pydantic = Depends(get_current_user)):  # type: ignore
    note = await Note.filter(id=note_id, author_id=user.id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found or you do not have access to it.")
    
    return await Note_Pydantic.from_tortoise_orm(note)



@router.delete('/note/{note_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_by_id(note_id: int, user: User_Pydantic = Depends(get_current_user)):  # type: ignore
    note = await Note.filter(id=note_id, author_id=user.id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found or you do not have access to it.")
    
    await note.delete()

    return


@router.put('/note/{note_id}', response_model=Note_Pydantic)
async def update_note(note_id: int, note_update: NoteIn_Pydantic, user: User_Pydantic = Depends(get_current_user)):  # type: ignore
    note = await Note.filter(id=note_id, author_id=user.id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found or you do not have access to it.")
    
    note.title = note_update.title
    note.body = note_update.body

    await note.save()

    return await Note_Pydantic.from_tortoise_orm(note)

@router.get('/download-notes')
async def downloadNotes(user: User_Pydantic = Depends(get_current_user)): # type: ignore
    notes_queryset = Note.filter(author_id=user.id)
    df = pd.DataFrame(await notes_queryset.values())

    buffer = io.StringIO()
    df.to_csv(buffer, index=False)

    response = Response(content=buffer.getvalue(), media_type='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=notes.csv'
    return response

