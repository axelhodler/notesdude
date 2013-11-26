% rebase layout
<p>Notes</p>
<form action="/new">
      <input type="submit" value="New Note">
</form>
<table border="1">
%for row in rows:
  <tr>
  %for col in row:
    <td>{{col}}</td>
  %end
  </tr>
%end
</table>