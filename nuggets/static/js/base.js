(function($) {

  templateObj = {
    toggleDeleteScreenshot: function(theID) {
      ssinput = 'screenshot_edit_' + theID.split('_')[2];

      if ($('#' + ssinput).attr('disabled')) {
        $('#' + ssinput).prop('disabled', false);
      }
      else {
          $('#' + ssinput).prop('disabled', true);
      }
    } // end toggleDeleteScreenshot
  } // end templateObj

  $(document).ready(function() {

    $('.screenshot_delete').click(function() {
      templateObj.toggleDeleteScreenshot($(this).attr('id'));
    });

  }); // end document.ready

}) (jQuery); // end main jQuery object
