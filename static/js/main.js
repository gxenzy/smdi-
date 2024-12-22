document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.getElementById('mainContent');
    const sidebarToggle = document.getElementById('sidebarToggle');

    // Hide sidebar initially
    hideSidebar();

    // Function to show sidebar and blur main content
    function showSidebar() {
        sidebar.style.transform = 'translateX(0)';
        mainContent.style.marginLeft = '250px'; // Adjust main content margin
        mainContent.classList.add('blurred'); // Add blur effect
    }

    // Function to hide sidebar and remove blur
    function hideSidebar() {
        sidebar.style.transform = 'translateX(-100%)';
        mainContent.style.marginLeft = '0'; // Remove margin when sidebar is hidden
        mainContent.classList.remove('blurred'); // Remove blur effect
    }

    // Toggle sidebar on button click
    sidebarToggle.addEventListener('click', function() {
        if (sidebar.style.transform === 'translateX(0)') {
            hideSidebar();
        } else {
            showSidebar();
        }
    });

    // Hide sidebar when mouse leaves the sidebar area
    sidebar.addEventListener('mouseleave', hideSidebar);

    // Show sidebar when mouse enters the left side of the window
    document.addEventListener('mousemove', function(e) {
        if (e.clientX < 50) { // Adjust this threshold as needed
            // Check if the sidebar is already visible to avoid repeated calls
            if (sidebar.style.transform === 'translateX(-100%)') {
                showSidebar();
            }
        }
    });

    // Optional: Hide sidebar when clicking outside (if desired)
    document.addEventListener('click', function(e) {
        if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
            hideSidebar();
        }
    });
});