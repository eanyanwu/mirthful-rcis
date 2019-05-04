console.log(authentication);


authentication.login('test_student', 'test_student',
    function(result) {
        console.log('Success', result);
    },
    function(status, error) {
        console.log(status, error);
    });
