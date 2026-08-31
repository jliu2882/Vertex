import { useState } from 'react'

interface TaskFormProps {
  onSubmit: (title: string, task_description: string) => void
  isSubmitting: boolean
}

function TaskForm({ onSubmit, isSubmitting }: TaskFormProps) {
  const [title, setTitle] = useState('')
  const [task_description, setTaskDescription] = useState('')

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (!title.trim()) return
    onSubmit(title, task_description)
    setTitle('')
    setTaskDescription('')
  }

  return (
    <form onSubmit={handleSubmit} className="task-form">
      <input
        className="task-form__input"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title"
      />
      <input
        className="task-form__input"
        value={task_description}
        onChange={(e) => setTaskDescription(e.target.value)}
        placeholder="Description (optional)"
      />
      <button type="submit" disabled={isSubmitting} className="task-form__submit">
        {isSubmitting ? 'Adding... ' : 'Add task'}
      </button>
    </form>
  )
}

export default TaskForm
