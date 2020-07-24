/**
 * Date: 2020. 07. 24.
 * Programmer: MH
 * Description: Code for making group alarm broadcast receiver
 */
package com.selab.coronamap.receiver;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import com.selab.coronamap.service.GroupAlertService;

public class GroupAlarmReceiver extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent intent) {
        Intent i = null;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O){    // If the version is higher than Oreo
            i = new Intent(context, GroupAlertService.class);   // To make intent for alert Service
            context.startForegroundService(i);      // For prevent doze state
        }else{
            i = new Intent(context, GroupAlertService.class);   // To make intent for alert Service
            context.startService(i);
        }
    }
}
