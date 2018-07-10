import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Comparator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Searches for the latest build of format Build-1.2.2.dmg.
 *
 * Implementation uses regexp and the latest supported build is Build-999.99.99.dmg.
 *
 * Usage:
 *  java LatestBuildUtil /path/to/builds/
 *
 */
public class LatestBuildUtil {

    private static String patternTemplate = "Build-(\\d{1,3})\\.*(\\d{0,2})\\.*(\\d{0,2}).dmg";
    private static Pattern pattern = Pattern.compile(patternTemplate);

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.out.println("Correct usage: \"java LatestBuildUtil /path/to/builds/\"");
            return;
        }

        Build latestBuild = Files.walk(Paths.get(args[0]))
                .filter(Files::isRegularFile)
                .map(Path::getFileName)
                .map(x -> new Build(x.toString()))
                .max(Comparator.naturalOrder())
                .get();

        System.out.println(latestBuild.originalPath);
    }

    static class Build implements Comparable<Build> {
        String originalPath;
        int major;
        int minor;
        int patch;

        Build(String path) {
            this.originalPath = path;
            Matcher matcher = pattern.matcher(path);
            if (matcher.matches()) {
                major = Integer.valueOf(matcher.group(1));
                String minorString = matcher.group(2);
                if (!minorString.isEmpty()) {
                    minor = Integer.valueOf(minorString);
                }
                String patchString = matcher.group(3);
                if (!patchString.isEmpty()) {
                    patch = Integer.valueOf(patchString);
                }
            }
        }

        @Override
        public int compareTo(Build other) {
            if (this.major > other.major) {
                return 1;
            } else if (this.major < other.major) {
                return -1;
            }
            if (this.minor > other.minor) {
                return 1;
            } else if (this.minor < other.minor) {
                return -1;
            }
            if (this.patch > other.patch) {
                return 1;
            } else if (this.patch < other.patch) {
                return -1;
            }
            return 0;
        }
    }
}

