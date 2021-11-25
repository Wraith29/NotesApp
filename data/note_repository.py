import sqlite3 as sql

from typing import List

from models.note import Note

class NoteRepository:
    def __init__(self, connectionString: str):
        self.conStr = connectionString
    
    def getAllNotes(self) -> List[Note]:
        query = "SELECT id, title, content FROM notes"
        con = sql.connect(self.conStr)
        cur = con.cursor()
        notes = [Note.noteFromTuple(note) for note in cur.execute(query).fetchall()]
        con.commit()
        con.close()
        return notes

    def getNoteById(self, id: int) -> Note:
        query = f"SELECT id, title, content FROM notes WHERE id='{id}'"
        con = sql.connect(self.conStr)
        cur = con.cursor()
        note = Note.noteFromTuple(cur.execute(query).fetchone())
        con.commit()
        con.close()
        return note
    
    def updateNote(self, note: Note) -> None:
        query = "UPDATE notes SET title = ?, content = ? WHERE id=?"
        con = sql.connect(self.conStr)
        cur = con.cursor()
        cur.execute(query, [note.title, note.content, note.id])
        con.commit()
        con.close()

    def createNote(self, note: Note) -> int:
        """Returns the ID of the created note"""
        query = "INSERT INTO notes (title, content) VALUES (?, ?)"
        con = sql.connect(self.conStr)
        cur = con.cursor()
        cur.execute(query, [note.title, note.content])
        id = cur.execute("SELECT last_insert_rowid()").fetchone()
        con.commit()
        con.close()
        return id[0]
    
    def deleteNote(self, id: int) -> None:
        query = "DELETE FROM notes WHERE id=?"
        con = sql.connect(self.conStr)
        cur = con.cursor()
        cur.execute(query, [id])
        con.commit()
        con.close()
