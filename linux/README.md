### Installation instructions for Linux:

1. Add the contents of finerty.txt to the end of the file /usr/share/X11/xkb/symbols/fi
  If you wish to customize the layout (switch keys etc.), that can be done here

2. In the finnish layout section of the file /usr/share/X11/xkb/rules/evdev.xml, paste the following:
```
<layout>
  <configItem>
    <name>fi</name>
    <!-- Keyboard indicator for Finnish layouts -->
    <shortDescription>fi</shortDescription>
    <description>Finnish</description>
    <countryList>
      <iso3166Id>FI</iso3166Id>
    </countryList>
    <languageList>
      <iso639Id>fin</iso639Id>
    </languageList>
  </configItem>
  <variantList>
```
3. In the same file, add the following variant to the list of variants ( <variantList> ).
```
<variant>
  <configItem>
    <name>finerty</name>
    <description>Finerty</description>
  </configItem>
</variant>
```
4. Finally, add the following to the list of variants (after the '! variant') in the file /usr/share/X11/xkb/rules/evdev.lst
```finerty          fi: Finerty (custom)```

Now Finerty should show up as one of the keyboard variants for Finnish.
