$(document).ready(function() {
    $("a[name='delete']").click(function() {
        var del_item = $(this);
        $('#deleteModal').modal('show'); 
        $('#delete').click(function() {
            location.href = del_item.attr("click_action");
        });
    });
});