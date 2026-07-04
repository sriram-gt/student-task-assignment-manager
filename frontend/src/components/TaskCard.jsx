import { updateTask, deleteTask } from "../services/api";

const priorityColors = {
  high: "bg-red-100 text-red-600",
  medium: "bg-yellow-100 text-yellow-600",
  low: "bg-green-100 text-green-600",
};

export default function TaskCard({ task, onUpdate, onDelete }) {
  const isOverdue =
    !task.completed &&
    task.due_date &&
    new Date(task.due_date) < new Date();

  const handleToggle = async () => {
    await updateTask(task.id, { completed: !task.completed });
    onUpdate();
  };

  const handleDelete = async () => {
    if (confirm("Delete this task?")) {
      await deleteTask(task.id);
      onDelete();
    }
  };

  return (
    <div className={`bg-white rounded-xl shadow p-4 border-l-4 ${task.completed ? "border-green-400 opacity-70" : isOverdue ? "border-red-500" : "border-blue-400"}`}>
      <div className="flex justify-between items-start">
        <div className="flex items-start gap-3">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggle}
            className="mt-1 cursor-pointer w-4 h-4 accent-blue-600"
          />
          <div>
            <h3 className={`font-semibold text-gray-800 ${task.completed ? "line-through text-gray-400" : ""}`}>
              {task.title}
            </h3>
            {task.description && (
              <p className="text-sm text-gray-500 mt-1">{task.description}</p>
            )}
            <div className="flex gap-2 mt-2 flex-wrap">
              <span className={`text-xs px-2 py-1 rounded-full font-medium ${priorityColors[task.priority]}`}>
                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)} Priority
              </span>
              {task.due_date && (
                <span className={`text-xs px-2 py-1 rounded-full ${isOverdue ? "bg-red-100 text-red-600" : "bg-gray-100 text-gray-600"}`}>
                  Due: {new Date(task.due_date).toLocaleDateString()}
                  {isOverdue && " ⚠ Overdue"}
                </span>
              )}
            </div>
          </div>
        </div>

        <button
          onClick={handleDelete}
          className="text-red-400 hover:text-red-600 text-sm ml-2"
        >
          ✕
        </button>
      </div>
    </div>
  );
}