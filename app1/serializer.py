from rest_framework import serializers
import re

class user_register(serializers.Serializer):

    first_name = serializers.CharField(required=True, max_length=20)
    last_name = serializers.CharField(required=True, max_length=20)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=8)

    print()

    def email_validation(self, mail):
        if not re.match(r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', mail):
            print("email")
            raise serializers.as_serializer_error("Email is not correct")
        
        return mail

    def pass_validation(self, password):
        if not re.match(r'^(?=.*\d)(?=.*[a-zA-Z])[a-zA-Z\d]{8,}$', password):  
            raise ValueError("Password must contain at least 8 characters, including both letters and digits")   

        return password
    
    def validate(self, data):
        print(data,"sfsfsfdd")
        print("in.................................")
        if 'email' in data:
            self.email_validation(data['email'])
        if 'password' in data:
            self.pass_validation(data['password']) 

        return data    


   