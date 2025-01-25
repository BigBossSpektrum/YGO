document.addEventListener('DOMContentLoaded', function() {
    const toggleBtn = document.getElementById('toggleSidebarBtn');
    const sidebar = document.getElementById('sidebar');
    // const content = document.querySelector('.content');

    toggleBtn.addEventListener('click', function() {
        sidebar.classList.toggle('minimized');
        // content.classList.toggle('sidebar-expanded');
    });
});
