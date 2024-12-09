// task_list.js
document.addEventListener("DOMContentLoaded", () => {
    const taskCards = document.querySelectorAll(".task-card");
    const columns = document.querySelectorAll(".task-column");

    taskCards.forEach(card => {
        card.addEventListener("dragstart", (e) => {
            e.dataTransfer.setData("text/plain", e.target.dataset.taskId);
        });
    });

    columns.forEach(column => {
        column.addEventListener("dragover", (e) => {
            e.preventDefault();
        });

        column.addEventListener("drop", async (e) => {
            e.preventDefault();
            const taskId = e.dataTransfer.getData("text/plain");
            const draggedCard = document.querySelector(`.task-card[data-task-id="${taskId}"]`);
            e.target.appendChild(draggedCard);

            // Update task status in the backend
            const newStatus = e.target.id.replace("-", " "); // Convert 'to-do' -> 'To Do'
            try {
                await fetch(`/tasks/update-status/${taskId}/`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": "{{ csrf_token }}",
                    },
                    body: JSON.stringify({ status: newStatus }),
                });
            } catch (err) {
                console.error("Failed to update task status:", err);
            }
        });
    });
});
