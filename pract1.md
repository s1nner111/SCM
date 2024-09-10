# Практическая работа №1


## Номер 1

~~~
grep '^[^:]*' /etc/passwd | cut -d: -f1 | sort
~~~

## Номер 2
~~~
awk '{print $1, $2}' /etc/protocols | sort -k2,2n | tail -n 5
~~~

## Номер 3

~~~
message="$1"

length=${#message}

border="+$(printf '%*s' "$((length + 2))" '' | tr ' ' '-')+"

echo "$border"
echo "| $message |"
echo "$border"
~~~

## Номер 4
основной код
~~~
grep -o -E '\b[_a-zA-Z][_a-zA-Z0-9]*\b' "$1" | sort | uniq
~~~

код программы hello.c
```
#include <stdio.h>

int main() {
    printf("Hello world")
    return 0;
}
```

## Номер 5

~~~
chmod +x $1
sudo cp $1 /usr/local/bin
~~~
