package com.selab.coronamap.classes;

import android.content.Context;
import android.util.Log;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.util.Date;
public class CommHelper {
    private final String URL = "203.253.21.227";
    private final String TAG = "ServerCoMM";
    public static RequestQueue requestQueue;

    public CommHelper(Context mContext){
        requestQueue = Volley.newRequestQueue(mContext);
    }
    public boolean sendUserInformation(String id, String name, Date birth){
        final boolean[] result = {false};
        StringRequest request = new StringRequest(Request.Method.POST, URL+"/api/register_user_info", new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Log.d(TAG, response);
                result[0] = true;
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                result[0] = false;
            }
        });
        return result[0];
    }
}
