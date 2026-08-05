export interface Task {
  id: number;
  user_id: number;
  title: string;
  task_description: string;
}

export interface TaskListResponse {
  items: Task[];
  page: number;
  limit: number;
  total: number;
  total_pages: number;
}
