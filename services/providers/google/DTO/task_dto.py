class TaskCreate(BaseModel):
    name: str
    description: str | None = None
    due_date: str | None = None