module.exports = {
    
    validatePhoneNumber: (phoneNumber) => {
        const regex = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
        return regex.test(phoneNumber)
    }
}