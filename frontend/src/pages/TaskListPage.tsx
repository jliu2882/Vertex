import { FormEvent, useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { getTasks, createTask, deleteTask, updateTask } from '../api/tasks'
import { useNavigate } from 'react-router-dom'
import { clearToken, getUsernameFromToken } from '../api/token'
import TaskForm from '../components/TaskForm'
import TaskItem from '../components/TaskItem'

function TaskList() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const username = getUsernameFromToken()

  function handleLogout() {
    clearToken()
    navigate('/login')
  }
  
  const [search, setSearch] = useState('')
  const [searchInput, setSearchInput] = useState('')
  const [page, setPage] = useState(1)
  const limit = 10

  const { data, isLoading, error } = useQuery({
    queryKey: ['tasks', page, search],
    queryFn: () => getTasks({ page, limit, q: search }),
    keepPreviousData: true,
  })

  const handleSearchSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setPage(1)
    setSearch(searchInput.trim())
  }

  const createMutation = useMutation({
    mutationFn: createTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const deleteMutation = useMutation({ //deleting one temporarily locks all from deleting
    mutationFn: deleteTask,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, updates }: { id: number; updates: { title?: string; task_description?: string | null } }) =>
      updateTask(id, updates),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    },
  })

  if (isLoading) return (
    <div className="page-shell">
      <div className="task-shell">
        <p className="page-subtitle">Loading your tasks...</p>
      </div>
    </div>
  )

  if (error) return (
    <div className="page-shell">
      <div className="task-shell">
        <p className="auth-error">Error loading tasks: {error.message}</p>
      </div>
    </div>
  )

  const tasks = data?.items ?? []
  const totalPages = data?.total_pages ?? 1

  return (
    <div className="page-shell">
      <div className="task-shell">
        <div className="task-header">
          <div>
            <span className="page-badge">Your tasks</span>
            <h1 className="page-title">{username ? `Welcome back, ${username}` : 'Keep everything in view'}</h1>
            <p className="page-subtitle">Add a new task and stay focused on what matters most.</p>
          </div>
          <button onClick={handleLogout} className="task-logout">Log out</button>
        </div>

        <form className="task-search" onSubmit={handleSearchSubmit}>
          <input
            type="search"
            placeholder="Search tasks"
            value={searchInput}
            onChange={(event) => setSearchInput(event.target.value)}
            className="task-search-input"
          />
          <button type="submit" className="task-search-button">Search</button>
          <button
            type="button"
            className="task-search-clear"
            disabled={!search && !searchInput}
            onClick={() => {
              setSearchInput('')
              setSearch('')
              setPage(1)
            }}
          >
            Clear
          </button>
        </form>

        <TaskForm
          onSubmit={(title, task_description) =>
            createMutation.mutate({ title, task_description })
          }
          isSubmitting={createMutation.isPending}
        />

        {tasks.length > 0 ? (
          <>
            <ul className="task-list">
              {tasks.map((task) => (
                <TaskItem
                  key={task.id}
                  task={task}
                  onDelete={(id) => deleteMutation.mutate(id)}
                  onUpdate={(id, updates) => updateMutation.mutate({ id, updates })}
                  isDeleting={deleteMutation.isPending}
                  isUpdating={updateMutation.isPending}
                />
              ))}
            </ul>

            <div className="task-pagination">
              <button
                type="button"
                disabled={page <= 1}
                onClick={() => setPage((current) => Math.max(current - 1, 1))}
              >
                Previous
              </button>
              <span>
                Page {page} of {totalPages}
              </span>
              <button
                type="button"
                disabled={page >= totalPages}
                onClick={() => setPage((current) => Math.min(current + 1, totalPages))}
              >
                Next
              </button>
            </div>
          </>
        ) : (
          <div className="task-empty-state">No tasks yet. Add your first one above.</div>
        )}
      </div>
    </div>
  )
}

export default TaskList