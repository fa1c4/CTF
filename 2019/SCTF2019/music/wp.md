# music

JEB open the apk and decompile bytecode
find the main logic
```java
@Override  // android.support.v7.app.AppCompatActivity
protected void onCreate(Bundle savedInstanceState) {
    super.onCreate(savedInstanceState);
    this.setContentView(0x7F09001D);  // layout:activity_main2
    this.editText = (EditText)this.findViewById(0x7F070036);  // id:editText
    this.button = (Button)this.findViewById(0x7F070022);  // id:button
    this.button.setOnClickListener(new View.OnClickListener() {
        @Override  // android.view.View$OnClickListener
        public void onClick(View view) {
            String s = Main2Activity.this.editText.getText().toString();
            Main2Activity.this.input = s;
            Intent intent1 = new Intent(Main2Activity.this, s.class);
            d main2Activity$d0 = new d(Main2Activity.this);
            Main2Activity.this.d = main2Activity$d0;
            Main2Activity.this.startService(intent1);
            d main2Activity$d1 = Main2Activity.this.d;
            Main2Activity.this.bindService(intent1, main2Activity$d1, 1);
        }
    });
}


public class s extends Service {
    public class b extends Binder {
        public String a(String b) {
            return new a().a(b);
        }

        public String b(String a) {
            return new c().a(a, this.a(this.d()));
        }

        public String d() {
            return new q(s.this.a).get();
        }

        public boolean g(String a) {
            return a.equals("C28BC39DC3A6C283C2B3C39DC293C289C2B8C3BAC29EC3A0C3A7C29A1654C3AF28C3A1C2B1215B53");
        }
    }
...
}


public class q {
    private h h;
    private Context mycontext;

    public q(Context context) {
        this.mycontext = context;
    }

    public String get() {
        String s = null;
        this.h = new h(this.mycontext, "sctf.db", null, 1);
        Cursor cursor0 = this.h.getWritableDatabase().query("SYC", null, null, null, null, null, null);
        if(cursor0.moveToFirst()) {
            do {
            label_4:
                s = cursor0.getString(cursor0.getColumnIndex("S1")) + cursor0.getString(cursor0.getColumnIndex("S2"));
                if(cursor0.moveToNext()) {
                    goto label_4;
                }

                break;
            }
            while(true);
        }

        cursor0.close();
        return s;
    }
}


public class a {
    public String a(String text) {
        return this.b(text);
    }

    public String b(String a) {
        if(a != null) {
            try {
                return p.a(MessageDigest.getInstance("MD5").digest(a.getBytes()));
            }
            catch(Exception e) {
                e.printStackTrace();
            }
        }

        return null;
    }
}


public class c {
    private static int m;

    static {
        c.m = 0x100;
    }

    public String a(String e, String f) {
        int v = c.m;
        int[] a = new int[v];
        byte[] b = new byte[v];
        for(int i = 0; i < c.m; ++i) {
            a[i] = i;
            b[i] = (byte)f.charAt(i % f.length());
        }

        int j = 0;
        for(int i = 0; true; ++i) {
            int v4 = c.m;
            if(i >= v4 - 1) {
                break;
            }

            j = (a[i] + j + b[i]) % v4;
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
        }

        char[] arr_c = e.toCharArray();
        char[] d = new char[e.length()];
        int i = 0;
        int j = 0;
        for(int k = 0; k < arr_c.length; ++k) {
            int v9 = c.m;
            i = (i + 1) % v9;
            j = (a[i] + j) % v9;
            int temp = a[i];
            a[i] = a[j];
            a[j] = temp;
            d[k] = (char)(arr_c[k] - i ^ ((char)a[(a[i] + a[i] % v9) % v9]));
        }

        return p.a(new String(d).getBytes());
    }
}
```

execution call trace: onCreate -> class_s -> class_q -> class_a -> class_c
read the string from `sctf.db` and c() processing, then equals to `C28BC39DC3A6C283C2B3C39DC293C289C2B8C3BAC29EC3A0C3A7C29A1654C3AF28C3A1C2B1215B53`

here we need Java String encodes the array to string then convert back to char array
can **correctly** get the flagenc array in this way

```java
public class Main
{
    public static void main(String[] args) 
    {
        byte[] enctob = new byte[]{-62, -117, -61, -99, -61, -90, -62, -125, -62, -77, -61, -99, -62, -109, -62, -119, -62, -72, -61, -70, -62, -98, -61, -96, -61, -89, -62, -102, 22, 84, -61, -81, 40, -61, -95, -62, -79, 33, 91, 83};       
        String bs = new String(enctob);
        char[] flagenc = bs.toCharArray();
        for (int i = 0; i < bs.length(); ++i) {
            System.out.printf("%d, ", (int)flagenc[i]);
        }
    }
}

// int flagenc[] = {139, 221, 230, 131, 179, 221, 147, 137, 184, 250, 158, 224, 231, 154, 22, 84, 239, 40, 225, 177, 33, 91, 83};
```

for `key`, use sqlit spy or some other tools to extract the S1.S2 string
