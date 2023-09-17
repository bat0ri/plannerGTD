
// Add Task Slide
$(function() {
    const btn = $('.slide-add-form');
    const form = $('.form-task-add');

    btn.on('click', function() {
        btn.hide();
        form.css('display', 'flex');
    });

});

const textarea = document.querySelector('.addtask_description_input');
const style = window.getComputedStyle(textarea);
const lineHeight = parseInt(style.lineHeight);

textarea.addEventListener('input', () => {
  const rows = textarea.value.split('\n').length;
  const newHeight = rows * lineHeight;
  textarea.style.height = `${newHeight}px`;
});
// Air Datepicker
new AirDatepicker('#airdatepicker', {
              //isMobile: true,
               autoClose: true,
               //timepicker: true,
            // Handle render process
            buttons: ['clear'],
            locale: {
                days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                daysMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
                months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                today: 'Today',
                clear: 'Clear',
                dateFormat: 'dd.MM.yyyy',
                firstDay: 0
            }
        });

new AirDatepicker('#airdatepicker-2', {
              //isMobile: true,
               autoClose: true,
               //timepicker: true,
            // Handle render process
            buttons: ['clear'],
            locale: {
                days: ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
                daysShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
                daysMin: ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa'],
                months: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
                monthsShort: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                today: 'Today',
                clear: 'Clear',
                dateFormat: 'dd.MM.yyyy',
                firstDay: 0
            }
        });


// Complete the editForm
$(function() {
    // при клике на задачу заполняем форму данными
    $('.task').on('click', function() {
    var taskId = $(this).data('task-id');
    var taskName = $(this).find('.task_name').text();
    var taskDesc = $(this).find('.task_description').text();
    var taskFinish = $(this).find('.task_date').attr('date');
    var taskCategory = $(this).find('.task_cat').text();
    $('form.edittask_section').css('display', 'flex');
    $('form.edittask_section').find('input[name="task"]').val(taskName);
    $('form.edittask_section').find('textarea[name="description"]').val(taskDesc);
    $('form.edittask_section').find('input[name="finish"]').val(taskFinish);
    $('form.edittask_section').find('input[name="task_id"]').val(taskId);
    $('form.edittask_section').find('select[name="category_edit"]').val(11);

    var selectedLabels = [];
    $(this).find('.task_labels').each(function() {
      var labPk = $(this).attr('lab_pk');
      if (labPk) {
        selectedLabels.push(labPk);
      }
    });

    $('#id_labels_edit').val(selectedLabels);
    $('#id_labels_edit').trigger('change');

    $(document).ready(function() {
        $('.select2-edit').select2();
    });
    });
});


// Ajax editForm
$(function() {
  // Обработчик отправки формы
  $('#edit-task-form').submit(function(event) {
    event.preventDefault(); // Отменяем отправку формы по умолчанию

    var form = $(this);
    var taskId = form.find('input[name="task_id"]').val();
    console.log("EDIT FORM: task_id = " + taskId);

    $.ajax({
      type: 'POST',
      url: form.attr('action').replace('0', taskId),
      data: form.serialize(),
      success: function(data) {
        // Обновляем задачу на странице без ее полной перезагрузки
        var taskDiv = $('.task[data-task-id="' + taskId + '"]');

        taskDiv.find('.task_labels').remove();

        taskDiv.find('.task_name').text(form.find('input[name="task"]').val());
        taskDiv.find('.task_description').text(form.find('textarea[name="description"]').val());
        taskDiv.find('.task_date').text(form.find('input[name="finish"]').val());

        var labels = form.find('select[name="labels-edit"] option:selected');
        for (var i = 0; i < labels.length; i++) {
          var label = $(labels[i]);
          var labelDiv = $('<div class="task_labels"></div>');
          labelDiv.attr('lab_pk', label.val());
          labelDiv.css('color', label.attr('color'));
          labelDiv.text(label.text());
          taskDiv.find('.task_date').before(labelDiv);

        }

      },
      error: function(jqXHR, textStatus, errorThrown) {
        console.log('AJAX Error: ' + textStatus + ' ' + errorThrown);
      }
    });
  });
});
const addLabelBtn = document.querySelector('.add_label_btn');
const addLabelForm = document.querySelector('.add_label_form_field');
const cancelBtn = document.querySelector('.cancel_label_form_btn');

addLabelBtn.addEventListener('click', () => {
  addLabelForm.style.display = 'flex';
});

cancelBtn.addEventListener('click', () => {
  addLabelForm.style.display = 'none';
});




