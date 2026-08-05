import { useState } from 'react'
import type { Task } from '../types/task'

interface TaskItemProps {
  task: Task
  onDelete: (id: number) => void
  onUpdate: (id: number, updates: { title?: string; task_description?: string | null }) => void
  isDeleting: boolean
  isUpdating: boolean
}

function TaskItem({ task, onDelete, onUpdate, isDeleting, isUpdating }: TaskItemProps) {
  const [isEditing, setIsEditing] = useState(false)
  const [title, setTitle] = useState(task.title)
  const [description, setDescription] = useState(task.task_description)

  function handleSave() {
    const trimmedTitle = title.trim()
    if (!trimmedTitle) return

    onUpdate(task.id, {
      title: trimmedTitle,
      task_description: description.trim(),
    })
    setIsEditing(false)
  }

  function handleCancel() {
    setTitle(task.title)
    setDescription(task.task_description)
    setIsEditing(false)
  }

  return (
    <li className="task-item">
      {isEditing ? (
        <div className="task-form">
          <input
            className="task-form__input"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Task title"
          />
          <input
            className="task-form__input"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
          />
          <div className="task-item__content">
            <button onClick={handleSave} disabled={isUpdating} className="task-form__submit">
              {isUpdating ? 'Saving...' : 'Save'}
            </button>
            <button onClick={handleCancel} className="task-logout">
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="task-item__content">
          <div>
            <p className="task-item__title">{task.title}</p>
            <p className="task-item__description">{task.task_description || 'No description provided.'}</p>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button onClick={() => setIsEditing(true)} className="task-logout">
              Edit
            </button>
            <button onClick={() => onDelete(task.id)} disabled={isDeleting} className="task-delete-button">
              {isDeleting ? 'Deleting...' : 'Delete'}
            </button>
          </div>
        </div>
      )}
    </li>
  )
}

export default TaskItem