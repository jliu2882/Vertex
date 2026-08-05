import { api } from "./client";
import type { Task, TaskListResponse } from "../types/task";

export function getTasks({
  page = 1,
  limit = 10,
  q,
}: {
  page?: number;
  limit?: number;
  q?: string;
}) {
  const params = new URLSearchParams();
  params.append("page", String(page));
  params.append("limit", String(limit));
  if (q) params.append("q", q);

  return api.get<TaskListResponse>(`/tasks?${params.toString()}`);
}

export function createTask(task: {
  title: string;
  task_description?: string | null;
}) {
  return api.post<Task>("/tasks", task);
}

export function updateTask(
  id: number,
  task: {
    title?: string;
    task_description?: string | null;
  },
) {
  return api.put<Task>(`/tasks/${id}`, task);
}

export function deleteTask(id: number) {
  return api.delete<void>(`/tasks/${id}`);
}
