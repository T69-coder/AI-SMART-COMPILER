from languages.java_engine import run_java

code = '''
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello Java");
    }
}
'''

result = run_java(code)

print(result)