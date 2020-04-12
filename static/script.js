
// validation for forms in both admin and Pharmaceutical
$(document).ready(function() {
  $("#reg").validate({
    rules: {
      name: {
        required: true,
        minlength: 4
      },
      username: {
        required: true,
        minlength: 7,
        maxlength: 15
      },
      email: {
        required: true,
        email: true
      },
      location: {
        required: true
      },
      drug_name: {
        required: true
      },
      uses: {
        required: true
      },
      side_effect: {
        required: true
      },
      password: {
        required: true,
        minlength: 8
      },
      con_password: {
        required: true,
        minlength: 8,
        equalTo: "[name='password']"
      }

    },
    messages: {
      name: {
        required: 'Enter your name',
        minlength: 'Name must be at least 4 characters'
      },
      username: {
        required: 'Enter your username',
        minlength: 'Username must be at least 7 characters',
        maxlength: 'Username must not be above 15 characters'
      },
      email: {
        required: 'Enter your email'
      },
      location: {
        required: 'Where is the company located'
      },
      drug_name: {
        required: 'Enter the name of the drug'
      },
      uses: {
        required: 'Enter the uses of the drug'
      },
      side_effect: {
        required: 'Enter the side effect(s) of the drug'
      },
      password: {
        required: 'Enter your password',
        minlength: 'Password must be at least 8 characters'
      },
      con_password: {
        required: 'Repeat your password',
        minlength: 'Password must be at least 8 characters',
        equalTo: 'Password not a match'
      }
    },
    submitHandler: function(form) {
      form.submit();
    }
  });

});
