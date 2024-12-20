/*=============== SHOW HIDDEN - PASSWORD ===============*/
const showHiddenPassword = (inputPassword, inputIcon) => {
    const input = document.getElementById(inputPassword),
          iconEye = document.getElementById(inputIcon)


    iconEye.addEventListener('click', () => {
      // Change password to text
      if (input.type === 'password') {
        // Switch to text
        input.type = 'text'
  
        // Add icon
        iconEye.classList.add('ri-eye-line')
  
        // Remove icon
        iconEye.classList.remove('ri-eye-off-line')
      }
      else {
        // Change to password
        input.type = 'password'
  
        // Remove icon
        iconEye.classList.remove('ri-eye-line')
  
        // Add icon
        iconEye.classList.add('ri-eye-off-line')
      }
    })
  }
  
  showHiddenPassword('password', 'input-icon')

  /* ///^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])

  var passwordValidation =document.getElementById("password");

  

    function validatePassword(){
      var sitepassREGEX=/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
      if(sitepassREGEX.test(passwordValidation.value)===true){
          return true;
      }
      else{
          return false;
      }
      } */



    /* function msg()
    {
      if(validatePassword() === true)
      {
        alert('success! ')
        
      }
      else 
      {
        alert('Minimum eight characters, at least one letter, one number and one special character')

      }
    } */