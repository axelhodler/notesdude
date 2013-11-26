% rebase layout
<p>Notes</p>
<form action="/new">
      <input type="submit" value="New Note">
</form>
<table border="1">
%for row in rows:
  <tr>
    <td>{{row.get('id')}}</td>
    <td>{{row.get('title')}}</td>
    <td>{{row.get('content')}}</td>
  </tr>
%end
</table>