package com.selab.coronamap.activity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;
import com.selab.coronamap.R;

public class SignupActivity extends AppCompatActivity {
    TextView reg_name, reg_age, reg_address, reg_livingdistance;
    Button btn_signup;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_signup);

        reg_name = findViewById(R.id.signup_name);
        reg_age = findViewById(R.id.signup_age);
        reg_address = findViewById(R.id.signup_address);
        reg_livingdistance = findViewById(R.id.signup_livingdistance);
        btn_signup = findViewById(R.id.btn_signup);
        btn_signup.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                String name = reg_name.getText().toString();
                int age = Integer.parseInt(reg_name.getText().toString());
                String address = reg_name.getText().toString();
                float livingdistance = Float.parseFloat(reg_name.getText().toString());

            }
        });
    }
}

