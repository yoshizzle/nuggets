(function($) {

  nuggetObj = {

  } // end nuggetObj

  $(document).ready(function() {

    $('.delete-nugget').bind('click', function() {
      if (confirm('Are you sure? This is a destructive operation.')) {
        window.location.replace($(this).attr('href'));
      } else {
        return false;
      }
    });

  }); // end document.ready

}) (jQuery); // end main jQuery object
